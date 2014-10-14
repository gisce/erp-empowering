# -*- coding: utf-8 -*-
from osv import osv, fields
from empowering.utils import none_to_false
from oorq.decorators import job
from amoniak import AmonConverter, check_response
from amoniak.utils import PoolWrapper


class GiscedataPolissa(osv.osv):
    _name = 'giscedata.polissa'
    _inherit = 'giscedata.polissa'

    _columns = {
        'etag': fields.char('ETag', size=50),
    }

    def wkf_activa(self, cursor, uid, ids):
        # Search for reactivations
        react = []
        noves = []
        for polissa in self.browse(cursor, uid, ids):
            if not polissa.etag:
                noves.append(polissa.id)
            elif not polissa.modcontractual_activa.active:
                react.append(polissa.id)
        # Call the parent
        res = super(GiscedataPolissa, self).wkf_activa(cursor, uid, ids)
        # Do the normals
        ids = list(set(ids) - set(react) - set(noves))
        if ids:
            self.empowering_patch(cursor, uid, [polissa.id])
        if noves:
            self.empowering_post(cursor, uid, noves)
        # Reactivations
        if react:
            self.empowering_post(cursor, uid, react, {'react': True})
        return res

    @job(queue='empowering')
    def empowering_patch(self, cursor, uid, ids, data=None, context=None):
        polissa_f = ['name', 'etag']
        em = self.pool.get('empowering.api').service
        result = []
        for polissa in self.read(cursor, uid, ids, polissa_f, context=context):
            if not polissa['etag']:
                self.empowering_post(cursor, uid, [polissa['id']])
                continue
            amon_converter = AmonConverter(PoolWrapper(self.pool, cursor, uid))
            if not data:
                data = amon_converter.contract_to_amon(polissa['id'])[0]
            res = em.contract(polissa['name']).update(data, polissa['etag'])
            result.append(none_to_false(res))
            if check_response(res, data):
                self.write(cursor, uid, [polissa['id']], {'etag': res['_etag']})
        return result

    @job(queue='empowering')
    def empowering_post(self, cursor, uid, ids, context=None):
        res = []
        amon_converter = AmonConverter(PoolWrapper(self.pool, cursor, uid))
        em = self.pool.get('empowering.api').service
        for pol in self.read(cursor, uid, ids, ['modcontractuals_ids', 'name']):
            first = True
            upd = []
            for modcon_id in reversed(pol['modcontractuals_ids']):
                amon_data = amon_converter.contract_to_amon(pol['id'], {
                    'modcon_id': modcon_id
                })[0]
                if first:
                    response = em.contracts().create(amon_data)
                    first = False
                else:
                    etag = upd[-1]['_etag']
                    response = em.contract(pol['name']).update(amon_data, etag)
                if check_response(response, amon_data):
                    upd.append(response)
            if upd:
                res.append(upd[-1])
                self.write(cursor, uid, [pol['id']], {'etag': upd[-1]['_etag']})
        return res

GiscedataPolissa()