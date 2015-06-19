# -*- coding: utf-8 -*-
from osv import osv, fields


class GiscedataPolissa(osv.osv):
    _name = 'giscedata.polissa'
    _inherit = 'giscedata.polissa'

    _columns = {
        'etag': fields.char('ETag', size=50)
    }

GiscedataPolissa()


class GiscedataPolissaModcontractual(osv.osv):
    _name = 'giscedata.polissa.modcontractual'
    _inherit = 'giscedata.polissa.modcontractual'

    _columns = {
        'empowering_profile': fields.many2one('empowering.modcontractual.profile', 'Empowering profile'),
        'empowering_service': fields.many2one('empowering.modcontractual.service', 'Empowering services'),
    }

    def write(self, cursor, uid, ids, vals, context=None):

        res = super(GiscedataPolissaModcontractual, self).write(cursor, uid, ids, vals,
                                                                context)
        # TODO: Check whether new EmpoweringProfile must be added (renting,...)
        return res

GiscedataPolissaModcontractual()