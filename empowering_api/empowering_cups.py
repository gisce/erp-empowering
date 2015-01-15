# -*- coding: utf-8 -*-
from osv import osv, fields


class EmpoweringCups(osv.osv):
    _name = 'giscedata.cups.ps'
    _inherit = 'giscedata.cups.ps'

    _columns = {
        'empowering': fields.boolean('Empowering enabled', propi="no"),
    }

    _defaults = {
        'empowering': lambda *a: False,
    }

EmpoweringCups()
