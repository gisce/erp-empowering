from osv import osv, fields


class GiscedataPolissa(osv.osv):
    _name = 'giscedata.polissa'
    _inherit = 'giscedata.polissa'

    _columns = {
        'empowering_profile_id': fields.many2one(
            'empowering.customize.profile',
            'Empowering Profile'
        )
    }

GiscedataPolissa()
