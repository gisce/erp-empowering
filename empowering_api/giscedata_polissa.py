# -*- coding: utf-8 -*-
from osv import osv, fields


class GiscedataPolissa(osv.osv):
    _name = 'giscedata.polissa'
    _inherit = 'giscedata.polissa'

    _columns = {
        'etag': fields.char('ETag', size=50),
    }

GiscedataPolissa()