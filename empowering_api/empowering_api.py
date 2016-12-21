# -*- coding: utf-8 -*-
import netsvc
from osv import osv, fields
from tools import config

from amoniak.utils import setup_logging as amon_setup_logging, setup_empowering_api


def log(msg, level=netsvc.LOG_INFO):
    logger = netsvc.Logger()
    logger.notifyChannel('empowering', level, msg)

class FakeEmpoweringService(object):
    def __init__(self):
        self.ot101_results = False
        self.ot103_results = False
        self.ot201_results = False
        self.ot503_results = False

class EmpoweringAPI(osv.osv):
    _name = 'empowering.api'

    def setup(self, cursor, uid, username=None, password=None, company_id=None,
              cert_file=None, version=None, context=None):
        if not context:
            context = {}
        amon_setup_logging()
        self.company_id = config.get('empowering_company', company_id)
        self.cert_file = config.get('empowering_cert', cert_file)
        self.version = config.get('empowering_version', version)
        self.username = config.get('empowering_username', username)
        self.password = config.get('empowering_password', password)

        emp_conf = {}
        if self.company_id:
            emp_conf['company_id'] = self.company_id
        if self.cert_file:
            emp_conf['cert_file'] = self.cert_file
            emp_conf['key_file'] = self.cert_file
        if self.version:
            emp_conf['version'] = self.version
        if self.username and self.password:
            emp_conf['username'] = self.username
            emp_conf['password'] = self.password

        try:
            self.service = setup_empowering_api(**emp_conf)
            log("Setting Up Empowering Service (%s). Company-Id: %s Cert file: %s"
                % (self.service.apiroot, self.service.company_id,
                   self.service.cert_file))
            for k, v in context.get('empowering_args', {}).items():
                log("%s => %s" % (k, v))
                setattr(self.service, k, v)
        except:
            self.service = FakeEmpoweringService()


    def __init__(self, pool, cursor):
        self.username = None
        self.password = None
        self.company_id = None
        self.cert_file = None
        self.service = None
        self.version = None
        self.setup(cursor, 1)
        super(EmpoweringAPI, self).__init__(pool, cursor)

EmpoweringAPI()


class EmpoweringCupsBuilding(osv.osv):
    _name = 'empowering.cups.building'
    _rec_name = 'cups_id'

    _columns = {
        'cups_id': fields.many2one('giscedata.cups.ps', 'CUPS', required=True,
                                   readonly=True, select=1),

        'meteringPointId': fields.integer('Metering point identifier'),

        'buildingConstructionYear': fields.integer('Building construction year'),
        'dwellingArea': fields.integer('Dwelling area'),
        'propertyType': fields.selection([('primary', 'Primary residence'),
                                          ('second', 'Second home')],
                                         'Property type'),
        'buildingType': fields.selection([('Single_house', 'Single house'),
                                          ('Apartment', 'Apartment')],
                                         'Building type'),
        'dwellingPositionInBuilding':  fields.selection([('first_floor', 'First floor'),
                                                         ('middle_floor', 'Middle floor'),
                                                         ('last_floor', 'Last floor'),
                                                         ('other', 'Other')],
                                                        'Dwelling position in building'),
        'dwellingOrientation': fields.selection([('S', 'South'),
                                                 ('SE', 'Southeast'),
                                                 ('E', 'East'),
                                                 ('NE', 'Northeast'),
                                                 ('N', 'North'),
                                                 ('NW', 'Northwest'),
                                                 ('W', 'West'),
                                                 ('SW', 'Southwest')],
                                                'Dwelling orientation'),
        'buildingWindowsType': fields.selection([('single_panel', 'Single panel'),
                                                 ('double_panel', 'Double panel'),
                                                 ('triple_panel', 'Triple panel'),
                                                 ('low_emittance', 'Low emittance'),
                                                 ('other', 'Other')],
                                                'Building windows type'),
        'buildingWindowsFrame': fields.selection([('PVC', 'PVC'),
                                                  ('wood', 'Wood'),
                                                  ('aluminium', 'Aluminium'),
                                                  ('steel', 'Steel'),
                                                  ('other', 'Other')],
                                                 'Building windows frame'),
        'buildingCoolingSource': fields.selection([('electricity', 'Electricity'),
                                                   ('gas', 'Gas'),
                                                   ('district_cooling', 'District cooling'),
                                                   ('other', 'Other'),
                                                   ('not_installed', 'Not installed')],
                                                  'Building cooling source'),
        'buildingHeatingSource': fields.selection([('electricity', 'Electricity'),
                                                   ('gas', 'Gas'),
                                                   ('gasoil', 'Gasoil'),
                                                   ('district_heating', 'District heating'),
                                                   ('biomass', 'Biomass'),
                                                   ('other', 'Other'),
                                                   ('not_installed', 'Not installed')],
                                                  'Building heating source'),
        'buildingHeatingSourceDhw': fields.selection([('electricity', 'Electricity'),
                                                      ('gas', 'Gas'),
                                                      ('gasoil', 'Gasoil'),
                                                      ('district_heating', 'District heating'),
                                                      ('biomass', 'Biomassa'),
                                                      ('other', 'Other')],
                                                     'Building heating source dhw'),
        'buildingSolarSystem': fields.selection([('PV', 'PV'),
                                                 ('solar_thermal_heating', 'Solar thermal heating'),
                                                 ('solar_thermal_DHW', 'Solar thermal DHW'),
                                                 ('PV_solar_thermal_DHW', 'PV + Solar thermal DHW'),
                                                 ('other', 'Other'),
                                                 ('not_installed', 'Not installed')],
                                                'Building solar system'),
        'electricVehicle': fields.boolean('Electric vehicle'),

    }

EmpoweringCupsBuilding()


class EmpoweringModcontractualProfile(osv.osv):
    _name = 'empowering.modcontractual.profile'
    _rec_name = 'modcontractual_id'

    _columns = {
        'modcontractual_id': fields.many2one('giscedata.polissa.modcontractual', 'Contract Modification', required=True,
                                             readonly=True, select=1),
        'totalPersonsNumber': fields.integer('Total persons number'),
        'minorPersonsNumber': fields.integer('Minor persons number'),
        'workingAgePersonsNumber': fields.integer('Working age persons number'),
        'retiredAgePersonsNumber': fields.integer('Retired age persons number'),
        'malePersonsNumber': fields.integer('Male persons number'),
        'femalePersonsNumber': fields.integer('Female persons number'),
        'eduLevel_prim': fields.integer('Primary education level persons number'),
        'eduLevel_sec': fields.integer('Secondary education level persons number'),
        'eduLevel_uni': fields.integer('University education level persons number'),
        'eduLevel_noStudies': fields.integer('No studies education level persons number')
    }

EmpoweringModcontractualProfile()


class EmpoweringModcontractualService(osv.osv):
    _name = 'empowering.modcontractual.service'

    _columns = {
        'modcontractual_id': fields.many2one('giscedata.polissa.modcontractual', 'Contract modification', required=True,
                                             readonly=True, select=1),
        'OT101': fields.char('OT101', size=100),
        'OT103': fields.char('OT103', size=100),
        'OT105': fields.char('OT105', size=100),
        'OT106': fields.char('OT106', size=100),
        'OT109': fields.char('OT109', size=100),
        'OT201': fields.char('OT201', size=100),
        'OT204': fields.char('OT204', size=100),
        'OT401': fields.char('OT401', size=100),
        'OT502': fields.char('OT502', size=100),
        'OT503': fields.char('OT503', size=100),
        'OT603': fields.char('OT603', size=100),
        'OT603g': fields.char('OT603g', size=100),
        'OT701': fields.char('OT701', size=100),
        'OT703': fields.char('OT703', size=100)
    }

EmpoweringModcontractualService()
