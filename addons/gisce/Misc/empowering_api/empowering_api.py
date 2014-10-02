# -*- coding: utf-8 -*-
import netsvc
from osv import osv
from tools import config

from .amon.utils import setup_logging as amon_setup_logging, setup_empowering_api


def log(msg, level=netsvc.LOG_INFO):
    logger = netsvc.Logger()
    logger.notifyChannel('empowering', level, msg)


class EmpoweringAPI(osv.osv):
    _name = 'empowering.api'

    company_id = 0
    cert_file = ''
    service = None
    version = 'v1'

    def setup(self, cursor, uid, company_id=None, cert_file=None,
              version=None, context=None):
        if not context:
            context = {}
        amon_setup_logging()
        self.company_id = company_id
        self.cert_file = cert_file
        self.version = version
        log("Setting Up Empowering Service (%s). Company-Id: %s Cert file: %s"
            % (self.version, self.company_id, self.cert_file))

        self.service = setup_empowering_api(
            company_id=self.company_id, key_file=self.cert_file,
            cert_file=self.cert_file, version=self.version
        )
        for k, v in context.get('empowering_args', {}).items():
            log("%s => %s" % (k, v))
            setattr(self.service, k, v)

    def __init__(self, pool, cursor):
        super(EmpoweringAPI, self).__init__(pool, cursor)
        company_id = config.get('empowering_company', 0)
        cert_file = config.get('empwoering_cert', '')
        version = config.get('empowering_version', 'v1')
        if company_id and cert_file:
            self.setup(cursor, 1, company_id, cert_file, version)

EmpoweringAPI()