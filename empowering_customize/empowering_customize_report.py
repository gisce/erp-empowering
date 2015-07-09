# -*- coding: utf-8 -*-

from c2c_webkit_report import webkit_report
from report import report_sxw
from tools import config
import pooler


class ReprtEmpoweringCustomize(webkit_report.WebKitParser):
    def create_single_pdf(self, cursor, uid, ids, data, report_xml, context=None):
        if len(ids) > 1:
            raise Exception("Empowering custom report only accepts list of one id")
        if context is None:
            context = {}
        if 'empowering_channel' not in context:
            raise Exception('empowering_channel code is not defined in context')
        parent = super(ReprtEmpoweringCustomize, self).create_single_pdf
        pool = pooler.get_pool(cursor.dbname)
        polissa = pool.get('giscedata.polissa').browse(cursor, uid, ids[0])
        channel_obj = pool.get('empowering.customize.profile.channel')
        channels_ids = channel_obj.search(cursor, uid, [
            ('profile_id.id', '=', polissa.empowering_profile_id.id),
            ('channel_id.code', '=', context['empowering_channel'])
        ])
        if channels_ids:
            channel = channel_obj.browse(cursor, uid, channels_ids[0])
            report_xml.report_webkit = channel.template_id.path
        else:
            report_xml.report_webkit = polissa.empowering_profile_id.default_template_id.path
        return parent(cursor, uid, ids, data, report_xml, context)


class report_webkit_html(report_sxw.rml_parse):
    def __init__(self, cursor, uid, name, context):
        super(report_webkit_html, self).__init__(cursor, uid, name,
                                                 context=context)
        if context is None:
            context = {}
        if 'period' not in context:
            raise Exception('period is not defined in the context')
        self.localcontext.update({
            'cursor': cursor,
            'uid': uid,
            'addons_path': config['addons_path'],
            'period': context['period'],
            'heman_url': config['heman_url']
        })


ReprtEmpoweringCustomize(
    'report.empowering.customize',
    'giscedata.polissa',
    False,
    parser=report_webkit_html
)
