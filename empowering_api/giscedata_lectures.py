from osv import osv, fields

class GiscedataLecturesComptador(osv.osv):
    _name = 'giscedata.lectures.comptador'
    _inherit = 'giscedata.lectures.comptador'

    def update_empowering_last_measure(self, cursor, uid, ids, last_measure, type_measure='empowering_last_measure'):
	#Default type_measure=empowering_last_measure (for back compatibility) can be empowering_last_f5d_measure and empowering_last_p5d_measure
        upd_ids = []
        for comp in self.read(cursor, uid, ids, [type_measure]):
            if last_measure > comp[type_measure]:
                upd_ids.append(comp['id'])
        self.write(cursor, uid, upd_ids, {
            type_measure: last_measure
        })
        return len(upd_ids)

    _columns = {
        'empowering_last_measure': fields.datetime('Last F1 meassure sent'),
        'empowering_last_f5d_measure': fields.datetime('Last F5D meassure sent'),
        'empowering_last_p5d_measure': fields.datetime('Last P5D meassure sent')
    }

GiscedataLecturesComptador()
