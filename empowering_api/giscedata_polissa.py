# -*- coding: utf-8 -*-
from osv import osv, fields


class GiscedataPolissa(osv.osv):
    _name = 'giscedata.polissa'
    _inherit = 'giscedata.polissa'

    _columns = {
        'empowering_contractId': fields.char('Empowering contractId', size=50),
        'etag': fields.char('ETag', size=50),
    }

GiscedataPolissa()


class GiscedataPolissaModcontractual(osv.osv):
    _name = 'giscedata.polissa.modcontractual'
    _inherit = 'giscedata.polissa.modcontractual'

    def write(self, cursor, uid, ids, vals, context=None):

        res = super(GiscedataPolissaModcontractual, self).write(cursor, uid, ids, vals,
                                                                context)

        # TODO: Check whether new EmpoweringProfile must be added (renting,...) or not (power increase,...)
        return res

    def create(self, cursor, uid, vals, context=None):

        # TODO: Update EmpowerinProfile update in order to link to new modcontractual.
        res = super(GiscedataPolissa, self).create(cursor, uid, vals, context)
        return res


GiscedataPolissaModcontractual()