# -*- coding: utf-8 -*-
from osv import osv, fields

class EmpoweringCupsQuarantine(osv.osv):
    _name = 'empowering.cups.quarantine'
    _columns = {
        'code': fields.integer('Code', required=True),      
        'active': fields.boolean('Active', required=True),
        'name': fields.char('Name', size=60, required=True),      
        'description': fields.char('Description', size=200, required=True)
    }

    _defaults = {
        'active': lambda *a: 1,
    }
EmpoweringCupsQuarantine()

class GiscedataCupsPs(osv.osv):
    _name = 'giscedata.cups.ps'
    _inherit = 'giscedata.cups.ps'

    _columns = {
        'empowering': fields.boolean('Empowering enabled', propi="no"),
        'empowering_quarantine': fields.many2one('empowering.cups.quarantine', 'Quarantine state', required=True)
    }

    _defaults = {
        'empowering': lambda *a: True,
        'empowering_quarantine': lambda *a: 0,
    }
GiscedataCupsPs()
