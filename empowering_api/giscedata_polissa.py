# -*- coding: utf-8 -*-
from osv import osv, fields
from sql.aggregate import Max


class GiscedataPolissa(osv.osv):
    _name = 'giscedata.polissa'
    _inherit = 'giscedata.polissa'

    def _fnc_empowering_last_invoice_measure(self, cursor, uid, ids, field_name, arg, context=None):
        if not context:
            context = {}
        res = dict.fromkeys(ids, False)
        q = self.pool.get('giscedata.lectures.comptador').q(cursor, uid)
        sql = q.select([
            'polissa',
            Max('empowering_last_measure'),
        ], group_by=('polissa', )).where([
            ('polissa', 'in', ids)
        ])
        cursor.execute(*sql)
        for row in cursor.fetchall():
            res[row[0]] = row[1]
        return res

    _columns = {
        'etag': fields.char('ETag', size=50),
        'empowering_last_invoice_measure': fields.function(
            _fnc_empowering_last_invoice_measure, type='datetime', method=True,
            string='Last F1 meassure sent'
        ),
        'empowering_last_profile_measure': fields.datetime('Last F5D meassure sent'),
        'empowering_profile': fields.many2one('empowering.modcontractual.profile', 'Empowering profile'),
        'empowering_service': fields.many2one('empowering.modcontractual.service', 'Empowering services')
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