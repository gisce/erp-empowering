from osv import osv, fields


class GiscedataLecturesComptador(osv.osv):
    _name = 'giscedata.lectures.comptador'
    _inherit = 'giscedata.lectures.comptador'

    def update_empowering_last_measure(self, cursor, uid, ids, last_measure):
        upd_ids = []
        for comp in self.read(cursor, uid, ids, ['empowering_last_measure']):
            if last_measure > comp['empowering_last_measure']:
                upd_ids.append(comp['id'])
        self.write(cursor, uid, upd_ids, {
            'empowering_last_measure': last_measure
        })
        return len(upd_ids)

    _columns = {
        'empowering_last_measure': fields.datetime('Last meassure sent')
    }

GiscedataLecturesComptador()