from osv import osv, fields


class GiscedataPolissa(osv.osv):
    _name = 'giscedata.polissa'
    _inherit = 'giscedata.polissa'

    _columns = {
        'empowering_profile_id': fields.many2one(
            'empowering.customize.profile',
            'Empowering Profile'
        ),
        'empowering_channels_log': fields.one2many(
            'empowering.customize.profile.channel.log',
            'contract_id',
            'Empowering Log'
        )
    }

GiscedataPolissa()
