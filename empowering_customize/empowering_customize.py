from osv import osv, fields


class EmpoweringCustomizeInterval(osv.osv):
    _name = 'empowering.customize.interval'

    def name_get(self, cursor, uid, ids, context=None):
        if context is None:
            context = {}
        names = []
        measures = dict(self._columns['measure'].selection)
        for interval in self.browse(cursor, uid, ids, context=context):
            name = measures.get(interval.measure, '')
            if interval.measure != 'on_demand':
                name = '{} {}'.format(interval.number, name)
            names.append((interval.id, name))
        return names

    _columns = {
        'number': fields.integer('Number'),
        'measure': fields.selection([
            ('on_demand', 'On demand'),
            ('days', 'Days'),
            ('weeks', 'Weeks'),
            ('months', 'Months')
            ], 'Unit of measure'
        )
    }

EmpoweringCustomizeInterval()


class EmpoweringCustomizeTemplate(osv.osv):
    _name = 'empowering.customize.template'
    _columns = {
        'name': fields.char('Name', size=256, required=True),
        'path': fields.char('Template path', size=256, required=True)
    }

EmpoweringCustomizeTemplate()


class EmpoweringCustomizeProfile(osv.osv):
    _name = 'empowering.customize.profile'
    _columns = {
        'name': fields.char('Name', size=256, required=True),
        'contracts_ids': fields.one2many(
            'giscedata.polissa',
            'empowering_profile_id',
            'Contracts'
        ),
        'default_template_id': fields.many2one(
            'empowering.customize.template', 'Template'
        ),
        'channels_ids': fields.one2many(
            'empowering.customize.profile.channel',
            'profile_id',
            'Channels'
        )
    }

EmpoweringCustomizeProfile()


class EmpoweringCustomizeChannel(osv.osv):
    _name = 'empowering.customize.channel'
    _columns = {
        'name': fields.char('Name', size=256, required=True),
        'code': fields.char('Code', size=32, required=True),
    }
EmpoweringCustomizeChannel()


class EmpoweringCustomizeProfileChannel(osv.osv):
    _name = 'empowering.customize.profile.channel'
    _rec_name = 'channel_id'
    _columns = {
        'profile_id': fields.many2one(
            'empowering.customize.profile',
            'Profile',
            required=True
        ),
        'channel_id': fields.many2one(
            'empowering.customize.channel',
            'Channel',
            required=True
        ),
        'template_id': fields.many2one(
            'empowering.customize.template',
            'Template',
            required=True
        ),
        'interval_id': fields.many2one(
            'empowering.customize.interval',
            'Interval'
        )
    }

EmpoweringCustomizeProfileChannel()


class EmpoweringCustomizeProfileChannelLog(osv.osv):
    _name = 'empowering.customize.profile.channel.log'
    _rec_name = 'contract_id'

    _columns = {
        'contract_id': fields.many2one(
            'giscedata.polissa',
            'Contract'
        ),
        'channel_id': fields.many2one(
            'empowering.customize.profile.channel',
            'Channel'
        ),
        'period': fields.integer('Period reported'),
        'last_generated': fields.datetime('Last generated'),
        'mail_id': fields.many2one(
            'poweremail.mailbox', 'Mail'
        ),
        'sent': fields.boolean('Sent'),
        'date_sent': fields.date('Date sent'),
        'folder': fields.selection([
            ('inbox', 'Inbox'),
            ('drafts', 'Drafts'),
            ('outbox', 'Outbox'),
            ('trash', 'Trash'),
            ('followup', 'Follow Up'),
            ('sent', 'Sent Items')], 'Folder'),
    }

    _defaults = {
        'sent': lambda *a: 0,
    }

    _order = 'last_generated desc'

EmpoweringCustomizeProfileChannelLog()
