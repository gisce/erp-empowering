# -*- coding: utf-8 -*-
from osv import osv, fields

class EmpoweringPriceIndexed(osv.osv):
    _name = 'empowering.price.indexed'

    def _ff_name(self, cursor, uid, context):
        # todo: ff to return a name of emp_price_indexed with 'TARIFF + COST'
        pass

    _columns = {
        'tarif_id': fields.char('Tariff'),
        'cost': fields.integer('FEE'),
        "name": fields.function(_ff_name, type="text", method=True, store=True, string="Name"),
        'empowering_price_indexed_last_push': fields.datetime("Last indexed group data push"),
    }

EmpoweringPriceIndexed()

