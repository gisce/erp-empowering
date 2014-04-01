# -*- coding: utf-8 -*-
from osv import osv
from oorq.decorators import job
from empowering.utils import (make_utc_timestamp, remove_none, make_uuid,
                              none_to_false)


class GiscedataLecturesComptador(osv.osv):
    _name = 'giscedata.lectures.comptador'
    _inherit = 'giscedata.lectures.comptador'

    trg_fields = ['polissa', 'data_alta', 'data_baixa', 'name']

    def create(self, cursor, uid, vals, context=None):
        compt_id = super(GiscedataLecturesComptador,
                         self).create(cursor, uid, vals, context=context)
        self.empowering_patch(cursor, uid, [compt_id], context)
        return compt_id

    def write(self, cursor, uid, ids, vals, context=None):
        res = super(GiscedataLecturesComptador,
                    self).write(cursor, uid, ids, vals, context=context)
        # Només actualizem si modifiquem algun valor que afecti a empowering
        if set(vals.keys()) & set(self.trg_fields):
            self.empowering_patch(cursor, uid, ids, context=context)
        return res

    def unlink(self, cursor, uid, ids, context=None):
        res = super(GiscedataLecturesComptador,
                    self).unlink(cursor, uid, ids, context=context)
        self.empowering_patch(cursor, uid, ids, context=context)
        return res

    def empowering_data(self, cursor, uid, polissa_ids, context=None):
        """
        "devices":
          [
            {
              "dateStart": "2013-10-11T16:37:05Z",
              "dateEnd": null,
              "deviceId": "c1810810-0381-012d-25a8-0017f2cd3574"
            }
          ],
        """
        polissa_obj = self.pool.get('giscedata.polissa')
        contracts = {}
        for polissa in polissa_obj.read(cursor, uid, polissa_ids,
                                        ['comptadors'], context=context):
            devices = []
            for comptador in self.read(cursor, uid, polissa['comptadors'],
                                       self.trg_fields):
                if hasattr(self, 'build_name_tg'):
                    compt_serial = self.build_name_tg(comptador['id'])
                else:
                    compt_serial = comptador['name']
                devices.append({
                    'dateStart': make_utc_timestamp(comptador['data_alta']),
                    'dateEnd': make_utc_timestamp(comptador['data_baixa']),
                    'deviceId': make_uuid('giscedata.lectures.comptador',
                                          compt_serial)
                })
            contracts[polissa['id']] = remove_none({
                'devices': devices
            }, context)
        return contracts

    @job(queue='empowering')
    def empowering_patch(self, cursor, uid, ids, context=None):
        polissa_obj = self.pool.get('giscedata.polissa')
        em = self.pool.get('empowering.api').service
        result = []
        polisses_ids = []
        for comptador in self.read(cursor, uid, ids, ['polissa']):
            polissa_id = comptador['polissa'][0]
            if polissa_id not in polisses_ids:
                polisses_ids.append(polissa_id)
        data = self.empowering_data(cursor, uid, polisses_ids, context=context)
        for contract in polissa_obj.read(cursor, uid, data.keys(),
                                         ['etag', 'name'], context=context):
            devices = data[contract['id']]
            res = em.contract(contract['name']).update(devices,
                                                       contract['etag'])
            result.append(none_to_false(res))
            polissa_obj.write(cursor, uid, [contract['id']], {
                'etag': res['etag']
            })
        return result

GiscedataLecturesComptador()