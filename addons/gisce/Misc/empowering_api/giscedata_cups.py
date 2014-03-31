# -*- coding: utf-8 -*-

from osv import osv


class GiscedataCupsPs(osv.osv):
    _name = 'giscedata.cups.ps'
    _inherit = 'giscedata.cups.ps'

    def write(self, cursor, uid, ids, vals, context=None):
        polissa_obj = self.pool.get('giscedata.polissa')
        res = super(GiscedataCupsPs, self).write(cursor, uid, ids, vals,
                                                  context=context)
        trigger_fields = [
            'id_municipi', 'id_poblacio', 'tv', 'nv', 'pnp', 'es', 'pt', 'pu',
            'cpo', 'cpa', 'dp'
        ]
        if set(vals.keys()) & set(trigger_fields):
            pols = polissa_obj.search(cursor, uid, [
                ('cups.id', 'in', ids),
                ('state', 'not in', ('esborrany', 'validar'))
            ])
            polissa_obj.empowering_patch(cursor, uid, pols, ['titular'])
        return res

GiscedataCupsPs()