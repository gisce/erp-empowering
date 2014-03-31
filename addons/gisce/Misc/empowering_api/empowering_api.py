# -*- coding: utf-8 -*-
import netsvc
from osv import osv
from tools import config

from empowering import Empowering


def log(msg, level=netsvc.LOG_INFO):
    logger = netsvc.Logger()
    logger.notifyChannel('empowering', level, msg)


class EmpoweringAPI(osv.osv):
    _name = 'empowering.api'

    company_id = 0
    cert_file = ''
    service = None

    def setup(self, cursor, uid, company_id=None, cert_file=None,
              context=None):
        if not context:
            context = {}
        self.company_id = company_id
        self.cert_file = cert_file
        log("Setting Up Empowering Service. Company-Id: %s Cert file: %s" % (
            self.company_id, self.cert_file))
        self.service = Empowering(self.company_id, self.cert_file,
                                  self.cert_file)
        for k, v in context.get('empowering_args', {}).items():
            log("%s => %s" % (k, v))
            setattr(self.service, k, v)

    def __init__(self, pool, cursor):
        super(EmpoweringAPI, self).__init__(pool, cursor)
        company_id = config.get('empowering_company', 0)
        cert_file = config.get('empwoering_cert', '')
        if company_id and cert_file:
            self.setup(cursor, 1, company_id, cert_file)

EmpoweringAPI()