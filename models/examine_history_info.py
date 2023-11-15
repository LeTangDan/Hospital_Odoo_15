from odoo import api, fields, models
from odoo.osv import expression
from odoo.exceptions import ValidationError

_state = [('new', 'Soạn thảo'), ('done', 'Hoàn thành'), ('close', 'Đóng')]


class ExamineHistoryInfo(models.Model):
    _name = 'examine_history_info'
    _rec_name = 'sick_persion_id'
    _order = 'examine_date desc, id desc'
    _description = 'Hồ sơ thăm khám'
    _inherit = ['mail.thread', 'private_data_company', 'delete_record']
    _default_name = 'Xác nhận xóa Hồ sơ khám'
    _inactive = True

    # Thông tin chung
    name = fields.Char(string=u'Mã đợt khám', readonly=True, default='New')
    sick_persion_id = fields.Many2one(comodel_name="sick_persion_info", string="Bệnh nhân", required=True)
    special_customer_id = fields.Many2one(comodel_name="special_customer", string="Bệnh nhân đặc biệt")
    examine_date = fields.Date(string="Ngày khám", default=fields.Date.today)
    re_examine_date = fields.Date(string="Hẹn tái khám")
    send_auto = fields.Selection(string="Gửi tự động", selection=[('1', 'Có'), ('2', 'Không')], default='1')
    medical_history = fields.Char(string="Tiền sử bệnh lý")
    allergy = fields.Char(string="Dị ứng")
    heartbeat = fields.Char(string="Nhịp tim")
    blood_pressure = fields.Char(string="Huyết áp")
    eye_sight = fields.Char(string="Thị lực")
    height = fields.Float(string="Chiều cao (cm)")
    weigh = fields.Float(string="Cân nặng (kg)")
    state = fields.Selection(string="Trạng thái", default='new', selection=_state)

    # Bệnh án
    doctor_id = fields.Many2one(comodel_name="doctor_info", string="Bác sĩ", default=lambda f: f.env['doctor_info'].search([], limit=1))
    test = fields.Text(string="Xét nghiệm")
    diagnose = fields.Text(string="Chẩn đoán")
    content = fields.Text(string="Nội dung khám")
    note = fields.Text(string="Ghi chú")
    file_upload = fields.Many2many('ir.attachment', 'examine_history_ir_attachment_rel',
                                   'examine_history_id', 'attachment_id', string='Tải lên')

    # Chi phí
    medicine_ids = fields.One2many(comodel_name="medicine_info_line", inverse_name="examine_line_id", string="Chi phí")
    amount = fields.Float(string="Tổng chi phí", digits=(16, 0))
    payment = fields.Float(string="Đã thanh toán", digits=(16, 0))
    debt = fields.Float(string="Còn nợ", digits=(16, 0))
    currency_id = fields.Many2one('res.currency', string='Tiền tệ', default=lambda f: f.env.company.currency_id.id)

    active = fields.Boolean(string="Active", default=True)
    schedule_examine_count = fields.Integer(string="Lịch hẹn", compute='_compute_schedule_examine_count')

    payment_history_ids = fields.One2many(comodel_name="payment_history", inverse_name="examine_line_id", string="Chi tiết thanh toán")

    def _compute_schedule_examine_count(self):
        schedule_examine = self.env['schedule_examine'].search([('examine_history_id', 'in', self.ids)])
        for line in self:
            line.schedule_examine_count = len(schedule_examine.filtered(lambda f: f.examine_history_id == line.id))

    def action_open_schedule_examine(self):
        schedule_examine = self.env['schedule_examine'].search([('examine_history_id', 'in', self.ids)])
        if not schedule_examine:
            return
        action = self.env.ref('hospital_management.action_schedule_examine_view').read()[0]
        domain = expression.AND([[], [('id', 'in', schedule_examine.ids)]])
        action['domain'] = domain
        return action

    @api.onchange('medicine_ids')
    def onchange_medicine_ids(self):
        _amount = 0.0
        for item in self.medicine_ids:
            _amount += item.amount
        self.amount = _amount

    @api.onchange('payment', 'amount')
    def onchange_payment(self):
        self.debt = self.amount - self.payment

    @api.onchange('sick_persion_id')
    def onchange_sick_persion_id(self):
        if self.sick_persion_id:
            # print(self.sick_persion_id)
            self.medical_history = self.sick_persion_id.medical_history
            # print(self.sick_persion_id.medical_history)
            # print(self.medical_history)
            self.allergy = self.sick_persion_id.allergy
            self.heartbeat = self.sick_persion_id.heartbeat
            self.blood_pressure = self.sick_persion_id.blood_pressure
            self.eye_sight = self.sick_persion_id.eye_sight
            self.height = self.sick_persion_id.height
            self.weigh = self.sick_persion_id.weigh
            self.special_customer_id = self.sick_persion_id.special_customer_ids[0] if self.sick_persion_id.special_customer_ids else False

    def btn_synchronize_medical_records(self):
        # print(self, 'baka')
        _val_sick_persion = {
            'medical_history': self.medical_history,
            'allergy': self.allergy,
            'heartbeat': self.heartbeat,
            'blood_pressure': self.blood_pressure,
            'eye_sight': self.eye_sight,
            'height': self.height,
            'weigh': self.weigh,
        }
        self.sick_persion_id.write(_val_sick_persion)
        schedule_examine = self.env['schedule_examine'].search([('re_examine_date', '=', self.examine_date), ('sick_persion_id', '=', self.sick_persion_id.id)], order='write_date desc', limit=1)
        if schedule_examine:
            schedule_examine.write({
                'state': 'done',
            })
        self.write({
            'state': 'done',
        })

    def re_open_draft(self):
        self.write({
            'state': 'new',
        })

    @api.constrains('examine_date', 're_examine_date')
    def _check_re_examine_date(self):
        for line in self:
            if line.examine_date and line.re_examine_date:
                if line.examine_date >= line.re_examine_date:
                    raise ValidationError('Ngày tái khám phải lớn hơn ngày khám')

    def name_get(self):
        result = []
        if self.env.context.get('close_view', False):
            for item in self:
                result.append((item.id, item.name))
        elif self.env.context.get('report_view', False):
            for item in self:
                result.append((item.id, f"{item.examine_date.strftime('%d/%m/%Y')} (Tổng tiền: {self.convert_number(str(int(item.amount)))})"))
        else:
            for item in self:
                result.append((item.id, f"{item.examine_date.strftime('%d/%m/%Y')} - {item.sick_persion_id.name}"))
        return result

    def convert_number(self, number=''):
        print(number)
        check = False
        if '-' in number:
            check = True
            number = number.strip('-')
        _len_num = len(number)
        _rev = list(reversed(number))
        _result = ''
        for item in range(0, _len_num):
            if item % 3 == 2:
                _result += _rev[item] + ','
            else:
                _result += _rev[item]
        _result = _result.strip(',')
        _return = list(reversed(_result))
        if check:
            return '-' + ''.join(_return)
        return f"{''.join(_return)} {self.currency_id.symbol}"

    @api.model_create_multi
    def create(self, values):
        for i in range(0, len(values)):
            if not values[i].get('name', False):
                values[i]['name'] = self.env['ir.sequence'].next_by_code('examine_history_code') or 'New'
        return super(ExamineHistoryInfo, self).create(values)

    def btn_edit_examine_history(self):
        self.ensure_one()
        view_id = self.env.ref('hospital_management.examine_history_info_form_view')
        return {
            'name': 'Hồ sơ',
            'type': 'ir.actions.act_window',
            'res_model': 'examine_history_info',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': view_id.id,
            'target': 'inline',
            'res_id': self.id,
        }

    def btn_done_payment(self):
        view_id = self.env.ref('hospital_management.payment_history_view_form_create')
        ctx = dict(self._context)
        ctx.update({
            'default_doctor_id': self.doctor_id.id,
            # 'default_doctor_id': self.doctor_id,
            'default_amount': self.debt,
            'default_examine_line_id': self.id,
        })
        return {
            'name': 'Thanh toán',
            'type': 'ir.actions.act_window',
            'res_model': 'payment_history',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': view_id.id,
            'target': 'new',
            'context': ctx,
        }

    def action_create_schedule_examine(self):
        view_id = self.env.ref('hospital_management.schedule_examine_form_view_create')
        ctx = dict(self._context)
        ctx.update({
            'default_sick_persion_id': self.sick_persion_id.id,
            'default_type': '2',
            'default_is_create': False,
            'default_examine_history_id': self.id,
        })
        return {
            'name': 'Lịch hẹn',
            'type': 'ir.actions.act_window',
            'res_model': 'schedule_examine',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': view_id.id,
            'target': 'new',
            'context': ctx,
        }

    def action_create_potential_patient(self):
        view_id = self.env.ref('hospital_management.potential_patient_view_form')
        ctx = dict(self._context)
        ctx.update({
            'default_sick_persion_id': self.sick_persion_id.id,
            'default_tinh_trang': self.diagnose,
            'default_ly_do': self.note,
        })
        return {
            'name': 'Bệnh nhân tiềm năng',
            'type': 'ir.actions.act_window',
            'res_model': 'potential_patient',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': view_id.id,
            'target': 'new',
            'context': ctx,
        }

    def action_create_special_customer(self):
        self.sick_persion_id.btn_create_special_customer()

    def action_view_history(self):
        return {
            'name': self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'examine_history_info',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref('hospital_management.view_history_examine_history_info').id,
            'target': 'current',
            'res_id': self.id,
            'context': dict(self._context),
        }

    def action_create_payment_history(self):
        values = []
        for item in self.search([('payment', '!=', 0), ('doctor_id', '!=', False)]).filtered(lambda f: not f.payment_history_ids):
            values.append({
                'examine_line_id': item.id,
                'amount': item.payment,
                'doctor_id': item.doctor_id.id,
                'date': item.examine_date,
            })
        if values:
            self.env['payment_history'].create(values)
