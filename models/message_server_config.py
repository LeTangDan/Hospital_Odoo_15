# -*- coding: utf-8 -*-
from odoo import api, fields, models
# import telerivet
from datetime import date, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class MessageServerConfig(models.Model):
    _name = 'message_server_config'
    _inherit = ['private_data_company']
    _rec_name = 'name'
    _description = 'Cấu hình SMS'

    name = fields.Char(string="API key")
    project_id = fields.Char(string="Project ID")

    def auto_sent_message(self):
        MessageServerConfig = self.env['message_server_config']
        ScheduleExamine = self.env['schedule_examine']
        sms_server = MessageServerConfig.search([])
        if not sms_server:
            return
        _time = date.today() + timedelta(days=1)
        _times = _time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        for item in sms_server:
            # connect = telerivet.API(item['name'])
            if not connect:
                return
            project = connect.initProjectById(item['project_id'])
            if not project:
                return
            _users = item.create_uid.company_id.user_ids.ids
            schedule_examine = ScheduleExamine.search([
                ('create_uid', 'in', _users),
                ('state', '=', 'waiting'),
                ('re_examine_date', '=', _time),
                ('send_auto', '=', '1'),
            ])
            if schedule_examine:
                for item1 in schedule_examine:
                    try:
                        project.sendMessage(
                            content=item1['name'],
                            to_number=item1['sick_persion_id']['phone']
                        )
                        item1.write({
                            'state': 'sent',
                        })
                    except Exception as e:
                        pass

    def btn_message_server_config(self):
        res_id = self.env['message_server_config'].search([], limit=1).id or False
        view_id = self.env.ref('hospital_management.message_server_config_form_view')
        return {
            'name': 'Cấu hình SMS',
            'type': 'ir.actions.act_window',
            'res_model': 'message_server_config',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': view_id.id,
            'target': 'new',
            'res_id': res_id,
        }

    def btn_done_ok(self):
        return {'type': 'ir.actions.act_window_close'}
