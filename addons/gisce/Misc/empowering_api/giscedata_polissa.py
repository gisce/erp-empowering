# -*- coding: utf-8 -*-
from osv import osv, fields
from empowering.service import Empowering
from empowering.utils import make_uuid, false_to_none, make_utc_timestamp, \
    none_to_false


def get_street_name(cups):
    street = []
    street_name = u''
    if cups.cpo or cups.cpa:
        street = u'CPO %s CPA %s' % (cups.cpo, cups.cpa)
    else:
        if cups.tv:
            street.append(cups.tv.name)
        if cups.nv:
            street.append(cups.nv)
        street_name += u' '.join(street)
        street = [street_name]
        for f_name, f in [(u'número', 'pnp'), (u'escalera', 'es'),
                          (u'planta', 'pt'), (u'puerta', 'pu')]:
            val = getattr(cups, f)
            if val:
                street.append(u'%s %s' % (f_name, val))
    street_name = ', '.join(street)
    return street_name


class GiscedataPolissa(osv.osv):
    _name = 'giscedata.polissa'
    _inherit = 'giscedata.polissa'

    _columns = {
        'etag': fields.char('ETag', size=50),
    }

    EMPOWERING_MAP = {
        'pagador': ['payerId'],
        'titular': ['ownerId'],
        'potencia': ['power'],
        'cups': ['customer', 'address', 'meteringPointId'],
        'comptadors': ['devices'],
        'cnae': ['activityCode'],
        'tarifa': ['tariffId'],

    }

    def wkf_activa(self, cursor, uid, ids):
        # Search for reactivations
        react = []
        noves = []
        for polissa in self.browse(cursor, uid, ids):
            if not polissa.etag:
                noves.append(polissa.id)
            elif not polissa.modcontractual_activa.active:
                react.append(polissa.id)
        # Call the parent
        res = super(GiscedataPolissa, self).wkf_activa(cursor, uid, ids)
        # Do the normals
        ids = list(set(ids) - set(react) - set(noves))
        if ids:
            # Busquem les diferències entre la modcon anterior i l'actual
            # per passar-ho per post
            for polissa in self.browse(cursor, uid, ids):
                changes = self.EMPOWERING_MAP.copy()
                self.empowering_patch(cursor, uid, [polissa.id], changes)
        if noves:
            self.empowering_post(cursor, uid, noves)
        # Reactivations
        if react:
            self.empowering_post(cursor, uid, react, {'react': True})
        return res

    def empowering_patch(self, cursor, uid, ids, vals, context=None):
        em = Empowering(8449512768)
        result = []
        for polissa in self.read(cursor, uid, ids, ['id', 'name', 'etag']):
            upd = set(vals.keys()) & set(self.EMPOWERING_MAP.keys())
            if upd:
                data = self.empowering_data(cursor, uid, ids, context)[0]
                # Try to get the differences
                keys_to_update = []
                for k in upd:
                    keys_to_update += self.EMPOWERING_MAP.get(k, [])
                for k in data.copy().keys():
                    if k not in keys_to_update:
                        del data[k]
                res = em.contract(polissa['name']).update(data,
                                                          polissa['etag'])
                result.append(none_to_false(res))
                self.write(cursor, uid, [polissa['id']], {'etag': res['etag']})
        return result

    def empowering_post(self, cursor, uid, ids, context=None):
        em = Empowering(8449512768)
        data = self.empowering_data(cursor, uid, ids, context)
        res = em.contracts().create(data)
        # Parse and assign etags
        for idx, resp in enumerate(res):
            self.write(cursor, uid, [ids[idx]], {'etag': resp['etag']})
        return res

    def empowering_data(self, cursor, uid, ids, context=None):
        """Converts contracts to AMON.

        {
          "payerId":"payerID-123",
          "ownerId":"ownerID-123",
          "signerId":"signerID-123",
          "power":123,
          "dateStart":"2013-10-11T16:37:05Z",
          "dateEnd":null,
          "contractId":"contractID-123",
          "customer":{
            "customerId":"payerID-123",
            "address":{
              "city":"city-123",
              "cityCode":"cityCode-123",
              "countryCode":"ES",
              "country":"Spain",
              "street":"street-123",
              "postalCode":"postalCode-123"
            }
          },
          "meteringPointId":"c1759810-90f3-012e-0404-34159e211070",
          "devices":[
            {
              "dateStart":"2013-10-11T16:37:05Z",
              "dateEnd":null,
              "deviceId":"c1810810-0381-012d-25a8-0017f2cd3574"
            }
          ],
          "version":1,
          "activityCode":"activityCode",
          "tariffId":"tariffID-123",
          "companyId":1234567890
        }
        """
        if not context:
            context = {}
        res = []
        modcon_obj = self.pool.get('giscedata.polissa.modcontractual')
        if not hasattr(ids, '__iter__'):
            ids = [ids]
        for polissa in self.browse(cursor, uid, ids, context):
            if 'modcon_id' in context:
                modcon = modcon_obj.get(context['modcon_id'])
            else:
                modcon = polissa.modcontractual_activa
            contract = {
                'companyId': 8449512768,
                'ownerId': make_uuid('res.partner', modcon.titular.id),
                'payerId': make_uuid('res.partner', modcon.pagador.id),
                'dateStart': make_utc_timestamp(modcon.data_inici),
                'dateEnd': make_utc_timestamp(modcon.data_final),
                'contractId': polissa.name,
                'tariffId': modcon.tarifa.name,
                'power': int(modcon.potencia * 1000),
                'version': int(modcon.name),
                'activityCode': modcon.cnae and modcon.cnae.name or None,
                'meteringPointId': make_uuid('giscedata.cups.ps',
                                             modcon.cups.name),
                'customer': {
                    'customerId': make_uuid('res.partner', modcon.titular.id),
                    'address': {
                        'city': polissa.cups.id_municipi.name,
                        'cityCode': polissa.cups.id_municipi.ine,
                        'countryCode': polissa.cups.id_provincia.country_id.code,
                        'street': get_street_name(polissa.cups),
                        'postalCode': polissa.cups.dp
                    }
                }
            }
            devices = []
            for comptador in polissa.comptadors:
                devices.append({
                    'dateStart': make_utc_timestamp(comptador.data_alta),
                    'dateEnd': make_utc_timestamp(comptador.data_baixa),
                    'deviceId': make_uuid('giscedata.lectures.comptador',
                                          comptador.id)
                })
            contract['devices'] = devices
            res.append(false_to_none(contract, context))
        return res

GiscedataPolissa()