from odoo import api, fields, models
from datetime import timedelta


class ScheduleExamine(models.Model):
    _name = 'schedule_examine'
    _inherit = ['private_data_company', 'delete_record']
    _rec_name = 'sick_persion_id'
    _description = 'Schedule Examine'
    _order = "re_examine_date desc"
    _default_name = 'Xác nhận xóa Lịch hẹn'
    _inactive = True

    name = fields.Text(string='Lời nhắn')
    sick_persion_id = fields.Many2one(comodel_name="sick_persion_info", string="Bệnh nhân", ondelete="restrict", required=True)
    re_examine_date = fields.Date(string="Ngày hẹn", default=fields.Date.today)
    state = fields.Selection(string="Trạng thái", selection=[('waiting', 'Đang chờ'), ('sent', 'Đã nhắc hẹn'), ('done', 'Đã khám'), ('cancel', 'Đã hủy lịch hẹn')], default='waiting')
    is_create = fields.Boolean(string="True", default=True)
    examine_history_id = fields.Integer(string="Hồ sơ", default=0)
    type = fields.Selection(string="Loại", selection=[('1', 'Hẹn khám'), ('2', 'Tái khám')], default='1')
    send_auto = fields.Selection(string="Gửi tự động", selection=[('1', 'Có'), ('2', 'Không')], default='1')
    active = fields.Boolean(string="Active", default=True)
    ly_do = fields.Char(string='Lý do')

    @api.onchange('re_examine_date')
    def onchange_re_examine_date(self):
        if self.re_examine_date:
            _time = self.re_examine_date + timedelta(hours=7)
            self.name = "Quý khách có lịch hẹn khám vào ngày %s" % (_time.strftime("%d/%m/%Y"),)

    def btn_done(self):
        self.state = 'done'

    def btn_cancel(self):
        self.state = 'cancel'

    def btn_refresh(self):
        self.state = 'waiting'

    @api.model_create_multi
    def create(self, values):
        for i in range(0, len(values)):
            values[i].update({
                'is_create': False
            })
        result = super(ScheduleExamine, self).create(values)
        for res in result:
            if res.examine_history_id:
                self.env['examine_history_info'].search([('id', '=', res.examine_history_id)]).write({'re_examine_date': res.re_examine_date})
        return result

    def write(self, values):
        if values.get('re_examine_date', False) and len(values) == 1:
            return
        result = super(ScheduleExamine, self.filtered(lambda f: f.company_id == f.env.company)).write(values)
        if values.get('re_examine_date', False):
            for line in self:
                self.env['examine_history_info'].search([('id', '=', line.examine_history_id)]).write({'re_examine_date': line.re_examine_date})
        return result
