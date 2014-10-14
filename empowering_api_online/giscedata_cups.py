# -*- coding: utf-8 -*-

from osv import osv
from amoniak import AmonConverter
from amoniak.utils import PoolWrapper


class GiscedataCupsPs(osv.osv):
    _name = 'giscedata.cups.ps'
    _inherit = 'giscedata.cups.ps'

    def write(self, cursor, uid, ids, vals, context=None):
        polissa_obj = self.pool.get('giscedata.polissa')
        res = super(GiscedataCupsPs, self).write(cursor, uid, ids, vals,
                                                  context=context)
        amon_converter = AmonConverter(PoolWrapper(self.pool, cursor, uid))
        trigger_fields = [
            'id_municipi', 'id_poblacio', 'tv', 'nv', 'pnp', 'es', 'pt', 'pu',
            'cpo', 'cpa', 'dp'
        ]
        if set(vals.keys()) & set(trigger_fields):
            pols = polissa_obj.search(cursor, uid, [
                ('cups.id', 'in', ids),
                ('state', 'not in', ('esborrany', 'validar'))
            ])
            for polissa_id in pols:
                data = amon_converter.contract_to_amon(polissa_id)[0]
                data = dict(meteringPointId=data['meteringPointId'],
                          customer=data['customer'])
                polissa_obj.empowering_patch(cursor, uid, pols, data)
        return res

GiscedataCupsPs()