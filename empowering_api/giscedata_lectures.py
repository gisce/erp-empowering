from osv import osv, fields


class GiscedataLecturesComptador(osv.osv):
    _name = 'giscedata.lectures.comptador'
    _inherit = 'giscedata.lectures.comptador'

    _columns = {
        'empowering_last_measure': fields.datetime('Last meassure sent')
    }

GiscedataLecturesComptador()