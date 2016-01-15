# -*- coding: utf-8 -*-
{
    "name": "Empowering API",
    "version": "0.2.1",
    "depends": ["base", "giscedata_polissa", "giscedata_lectures"],
    "author": "GISCE-TI, S.L.",
    "category": "Misc",
    "description": """
    This module provide :
        * Integration between Empowering service
    """,
    "init_xml": [],
    'update_xml': ["giscedata_polissa_view.xml", "security/empowering_api_security.xml",
                   "security/ir.model.access.csv", "giscedata_cups_data.xml"],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
