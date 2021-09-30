# -*- coding: utf-8 -*-
from osv import osv, fields

class EmpoweringPriceIndexed(osv.osv):
    _name = 'empowering.price.indexed'
    _order = 'empowering_price_indexed_last_push desc'

    _columns = {
        'etag': fields.char('ETag', size=50),
        'tariff_id': fields.char('Tariff', size=64, required=True),
        'cost': fields.integer('FEE', required=True),
        'empowering_price_indexed_last_push': fields.datetime("Last indexed group data push"),
    }

    _sql_constraints = [('name_uniq', 'unique (tariff_id, cost)', u'Duplicated empowering price indexed group')]

EmpoweringPriceIndexed()

