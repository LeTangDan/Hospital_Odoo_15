from odoo import api, fields, models, _
# import telerivet
from odoo.exceptions import Warning


class SendMsgWizard(models.TransientModel):
    _name = 'send_msg_wizard'
    _description = 'Send Msg Wizard'

    schedule_examine_ids = fields.Many2many("schedule_examine", "ref_m2m_smw_se", "smw_id", "se_id", "Schedule Examine")

    def btn_confirm_send(self):
        if not self.schedule_examine_ids:
            raise Warning(_('Vui lòng chọn lịch hẹn cần gửi tin !!!'))
        sms_server = self.env['message_server_config'].search([], limit=1)
        if not sms_server:
            raise Warning(_('Vui lòng kiểm tra lại Cài đặt SMS !!!'))
        # connect = telerivet.API(sms_server['name'])
        if not connect:
            raise Warning(_('Vui lòng kiểm tra lại Cài đặt SMS !!!'))
        project = connect.initProjectById(sms_server['project_id'])
        if not project:
            raise Warning(_('Vui lòng kiểm tra lại Cài đặt SMS !!!'))
        for item1 in self.schedule_examine_ids:
            try:
                project.sendMessage(content=item1['name'], to_number=item1['sick_persion_id']['phone'])
                item1.write({
                    'state': 'sent',
                })
            except Exception as e:
                print(e)
                pass
        return {'type': 'ir.actions.act_window_close'}
