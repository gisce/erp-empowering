# -*- coding: utf-8 -*-
from osv import osv
from oorq.decorators import job
from .amon import AmonConverter
from .amon.utils import PoolWrapper


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


    @job(queue='empowering')
    def empowering_patch(self, cursor, uid, ids, context=None):
        polissa_obj = self.pool.get('giscedata.polissa')
        patch = polissa_obj.empowering_patch
        result = []
        polisses_ids = []
        polissa_fields = ['etag', 'name', 'comptadors']
        for comptador in self.read(cursor, uid, ids, ['polissa']):
            polissa_id = comptador['polissa'][0]
            if polissa_id not in polisses_ids:
                polisses_ids.append(polissa_id)
        amon_converter = AmonConverter(PoolWrapper(self.pool, cursor, uid))
        for contract in polissa_obj.read(cursor, uid, polisses_ids,
                                         polissa_fields, context=context):
            data = amon_converter.device_to_amon(contract['comptadors'])
            devices = {'devices': data}
            result += patch(cursor, uid, [contract['id']], devices)
        return result

GiscedataLecturesComptador()