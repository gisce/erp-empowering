from osv import osv, fields
from addons import get_module_resource


class GiscedataLecturesComptador(osv.osv):
    _name = 'giscedata.lectures.comptador'
    _inherit = 'giscedata.lectures.comptador'

    def copy_data(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default.update({
            'empowering_last_measure': False,
            'empowering_last_f5d_measure': False,
            'empowering_last_p5d_measure': False
        })
        res = super(GiscedataLecturesComptador, self).copy_data(
            cr, uid, id, default, context
        )
        return res

    def update_empowering_measure(self, cursor, uid, ids, last_measure, type_measure):
        upd_ids = []
        for comp in self.read(cursor, uid, ids, [type_measure]):
            if last_measure > comp[type_measure]:
                upd_ids.append(comp['id'])
        self.write(cursor, uid, upd_ids, {
            type_measure: last_measure
        })
        return len(upd_ids)

    def update_empowering_last_measure(self, cursor, uid, ids, last_measure,
                                       type_measure='empowering_last_measure'):
        return self.update_empowering_measure(
            cursor, uid, ids, last_measure, type_measure
        )

    def update_empowering_last_f5d_measure(self, cursor, uid, ids, last_measure):
        return self.update_empowering_measure(
            cursor, uid, ids, last_measure, 'empowering_last_f5d_measure'
        )

    def update_empowering_last_p5d_measure(self, cursor, uid, ids, last_measure):
        return self.update_empowering_measure(
            cursor, uid, ids, last_measure, 'empowering_last_p5d_measure'
        )

    def get_aggregated_measures(self, cursor, uid, ids, date_start):
        sql_path = get_module_resource(
            'empowering_api', 'sql', 'aggregated_measures.sql'
        )
        with open(sql_path, 'r') as f:
            cursor.execute(f.read(), {
                'ids': tuple(ids), 'date_start': date_start
            })
        result = cursor.dictfetchall()
        return result

    _columns = {
        'empowering_last_measure': fields.datetime('Last F1 meassure sent'),
        'empowering_last_f5d_measure': fields.datetime('Last F5D meassure sent'),
        'empowering_last_p5d_measure': fields.datetime('Last P5D meassure sent')
    }


GiscedataLecturesComptador()
