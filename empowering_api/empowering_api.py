# -*- coding: utf-8 -*-
import netsvc
from osv import osv
from tools import config

from amoniak.utils import setup_logging as amon_setup_logging, setup_empowering_api


def log(msg, level=netsvc.LOG_INFO):
    logger = netsvc.Logger()
    logger.notifyChannel('empowering', level, msg)


class EmpoweringAPI(osv.osv):
    _name = 'empowering.api'

    def setup(self, cursor, uid, company_id=None, cert_file=None,
              version=None, context=None):
        if not context:
            context = {}
        amon_setup_logging()
        self.company_id = config.get('empowering_company', company_id)
        self.cert_file = config.get('empowering_cert', cert_file)
        self.version = config.get('empowering_version', version)

        emp_conf = {}
        if self.company_id:
            emp_conf['company_id'] = self.company_id
        if self.cert_file:
            emp_conf['cert_file'] = self.cert_file
            emp_conf['key_file'] = self.cert_file
        if self.version:
            emp_conf['version'] = self.version

        self.service = setup_empowering_api(**emp_conf)
        log("Setting Up Empowering Service (%s). Company-Id: %s Cert file: %s"
            % (self.service.apiroot, self.service.company_id,
               self.service.cert_file))
        for k, v in context.get('empowering_args', {}).items():
            log("%s => %s" % (k, v))
            setattr(self.service, k, v)

    def __init__(self, pool, cursor):
        self.company_id = None
        self.cert_file = None
        self.service = None
        self.version = None
        self.setup(cursor, 1)
        super(EmpoweringAPI, self).__init__(pool, cursor)

EmpoweringAPI()
