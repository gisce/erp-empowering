# -*- coding: utf-8 -*-
from osv import osv, fields
from empowering.utils import make_uuid, remove_none, make_utc_timestamp, \
    none_to_false
from oorq.decorators import job


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
                modcon_id = polissa.modcontractual_activa.modcontractual_ant
                modcon_id = modcon_id and modcon_id.id or False
                ctx = {}
                if modcon_id:
                    ctx['modcon_id'] = modcon_id
                changes = polissa.get_changes(context=ctx).keys()
                self.empowering_patch(cursor, uid, [polissa.id], changes)
        if noves:
            self.empowering_post(cursor, uid, noves)
        # Reactivations
        if react:
            self.empowering_post(cursor, uid, react, {'react': True})
        return res

    @job(queue='empowering')
    def empowering_patch(self, cursor, uid, ids, fields, context=None):
        em = self.pool.get('empowering.api').service
        result = []
        for polissa in self.browse(cursor, uid, ids, context=context):
            data = polissa.empowering_data(fields, context=context)[0]
            res = em.contract(polissa.name).update(data, polissa.etag)
            result.append(none_to_false(res))
            self.write(cursor, uid, [polissa.id], {'etag': res['etag']})
        return result

    @job(queue='empowering')
    def empowering_post(self, cursor, uid, ids, context=None):
        em = self.pool.get('empowering.api').service
        data = self.empowering_data(cursor, uid, ids, context)
        res = em.contracts().create(data)
        # https://github.com/nicolaiarocci/eve/commit/8dd330d9ea7f961f977df642aeea8d846eca48a2
        if isinstance(res, dict):
            res = [res]
        # Parse and assign etags
        for idx, resp in enumerate(res):
            self.write(cursor, uid, [ids[idx]], {'etag': resp['etag']})
        return res


    def empowering_data(self, cursor, uid, ids, fields=None, context=None):
        """Converts contracts to AMON.

        {
          "payerId": "payerID-123",
          "ownerId": "ownerID-123",
          "signerId": "signerID-123",
          "power": 123,
          "dateStart": "2013-10-11T16:37:05Z",
          "dateEnd": null,
          "contractId": "contractID-123",
          "customer":
          {
            "customerId": "payerID-123",
            "address":
            {
              "buildingId": "building-123"
              "city": "city-123",
              "cityCode": "cityCode-123",
              "countryCode": "ES",
              "country": "Spain",
              "street": "street-123",
              "postalCode": "postalCode-123"
            },
            "profile":
            {
                "totalPersonsNumber": 3,
                "minorsPersonsNumber": 0
                "workingAgePersonsNumber": 2,
                "retiredAgePersonsNumber": 1,
                "malePersonsNumber": 2,
                "femalePersonsNumber": 1,
                "educationLevel": {
                    "edu_prim" : 0,
                    "edu_sec" : 1,
                    "edu_uni" : 1,
                    "edu_noStudies" : 1
                }
            }
          },
          "meteringPointId": "c1759810-90f3-012e-0404-34159e211070",
          "devices":
          [
            {
              "dateStart": "2013-10-11T16:37:05Z",
              "dateEnd": null,
              "deviceId": "c1810810-0381-012d-25a8-0017f2cd3574"
            }
          ],
          "version": 1,
          "activityCode": "activityCode",
          "tariffId": "tariffID-123"
        }
        """
        if not context:
            context = {}
        res = []
        modcon_obj = self.pool.get('giscedata.polissa.modcontractual')
        cups_obj = self.pool.get('giscedata.cups.ps')
        if not hasattr(ids, '__iter__'):
            ids = [ids]
        if fields:
            fields += ['modcontractual_activa', 'data_inici', 'data_final',
                       'name']
            if 'titular' in fields and 'cups' not in fields:
                fields += ['cups']
        for polissa in self.read(cursor, uid, ids, fields, context=context):
            if 'modcon_id' in context:
                modcon_id = modcon_obj.get(context['modcon_id'])
            else:
                modcon_id = polissa['modcontractual_activa'][0]
            modcon = modcon_obj.read(cursor, uid, modcon_id, fields)
            contract = {
                'dateStart': make_utc_timestamp(modcon['data_inici']),
                'dateEnd': make_utc_timestamp(modcon['data_final']),
                'version': int(modcon['name']),
            }
            if 'titular' in modcon:
                contract['ownerId'] = make_uuid('res.partner',
                                                modcon['titular'][0])
                cups = cups_obj.browse(cursor, uid, modcon['cups'][0])
                contract['customer'] = {
                    'customerId': make_uuid('res.partner',
                                            modcon['titular'][0]),
                    'address': {
                        'city': cups.id_municipi.name,
                        'cityCode': cups.id_municipi.ine,
                        'countryCode': cups.id_provincia.country_id.code,
                        'street': get_street_name(cups),
                        'postalCode': cups.dp
                    }
                }
            if 'pagador' in modcon:
                contract['payerId'] = make_uuid('res.partner',
                                                modcon['pagador'][0])
            if 'name' in polissa:
                contract['contractId'] = polissa['name']
            if 'tarifa' in modcon:
                contract['tariffId'] = modcon['tarifa'][1]
            if 'potencia' in modcon:
                contract['power'] = int(modcon['potencia'] * 1000)
            if 'cnae' in modcon and modcon.get('cnae', False):
                contract['activityCode'] = modcon['cnae'][1]
            if 'cups' in modcon:
                contract['meteringPointId'] = make_uuid('giscedata.cups.ps',
                                                        modcon['cups'][1])
            res.append(remove_none(contract, context))
        return res

GiscedataPolissa()