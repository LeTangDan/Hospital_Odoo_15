from odoo import api, fields, models
from . import lib_default_avatar
from odoo.osv import expression

_nation = [
    ("1", 'Kinh'),
    ("2", "Tày"),
    ("3", "Thái"),
    ("4", "Mường"),
    ("5", "H'mông"),
    ("6", "Khmer"),
    ("7", "Nùng"),
    ("8", "Dao"),
    ("9", "Hoa"),
    ("10", "Người Jrai"),
    ("11", "Ê Đê"),
    ("12", "Ba Na"),
    ("13", "Xơ Đăng"),
    ("14", "Sán Chay"),
    ("15", "Cơ Ho"),
    ("16", "Sán Dìu"),
    ("17", "Chăm"),
    ("18", "Hrê"),
    ("19", "Ra Glai"),
    ("20", "M'Nông"),
    ("21", "Stiêng"),
    ("22", "Bru-Vân Kiều"),
    ("23", "Thổ"),
    ("24", "Khơ Mú"),
    ("25", "Cơ Tu"),
    ("26", "Giáy"),
    ("27", "Giẻ Triêng"),
    ("28", "Tà Ôi"),
    ("29", "Mạ"),
    ("30", "Co"),
    ("31", "Chơ Ro"),
    ("32", "Xinh Mun"),
    ("33", "Hà Nhì"),
    ("34", "Chu Ru"),
    ("35", "Lào"),
    ("36", "Kháng"),
    ("37", "La Chí"),
    ("38", "Phù Lá"),
    ("39", "La Hủ"),
    ("40", "La Ha"),
    ("41", "Pà Thẻn"),
    ("42", "Chứt"),
    ("43", "Lự"),
    ("44", "Lô Lô"),
    ("45", "Mảng"),
    ("46", "Cờ Lao"),
    ("47", "Bố Y"),
    ("48", "Cống"),
    ("49", "Ngái"),
    ("50", "Si La"),
    ("51", "Pu Péo"),
    ("52", "Rơ măm"),
    ("53", "Brâu"),
    ("54", "Ơ Đu")
]
_gender = [('nam', 'Nam'), ('nu', 'Nữ'), ('khac', 'Khác')]


class SickPersionInfo(models.Model):
    _name = 'sick_persion_info'
    _rec_name = 'name_res'
    _description = 'Thông tin bệnh nhân'
    _inherit = ['mail.thread', 'private_data_company']

    # Thông tin chung
    avatar = fields.Binary(string="Ảnh đại diện", attachment=True, default=lib_default_avatar._default_image())
    code = fields.Char(string="Mã bệnh nhân", readonly=True, default='New')
    name = fields.Char(string=u'Họ tên')
    gender = fields.Selection(string="Giới tính", default="nam", selection=_gender)
    nation = fields.Selection(string="Dân tộc", selection=_nation, default="1")
    age = fields.Integer(string="Tuổi", compute='_compute_age', store=True)
    birth_day = fields.Date(string="Ngày sinh")
    address = fields.Char(string="Địa chỉ")
    phone = fields.Char(string="Điện thoại", copy=False)
    mail = fields.Char(string="Mail")
    profession = fields.Char(string="Nghề nghiệp")
    note = fields.Text(string="Ghi chú")
    name_res = fields.Char(string="Name", compute='_compute_name', store=True)

    # Thông tin thăm khám
    examine_date = fields.Date(string="Ngày khám gần nhất", compute='_compute_date')
    re_examine_date = fields.Date(string="Hẹn tái khám", compute='_compute_date')
    medical_history = fields.Char(string="Tiền sử bệnh lý")
    allergy = fields.Char(string="Dị ứng")
    heartbeat = fields.Char(string="Nhịp tim")
    blood_pressure = fields.Char(string="Huyết áp")
    eye_sight = fields.Char(string="Thị lực")
    height = fields.Float(string="Chiều cao (cm)")
    weigh = fields.Float(string="Cân nặng (kg)")
    examine_history_ids = fields.One2many(comodel_name="examine_history_info", inverse_name="sick_persion_id", string="Hồ sơ thăm khám", required=False)
    customer_type_id = fields.Many2one(comodel_name="customer_type", string="Loại bệnh nhân", ondelete="restrict")
    special_customer_ids = fields.One2many(comodel_name="special_customer", inverse_name="sick_persion_id", string="BNDB")
    schedule_examine_count = fields.Integer(string="Lịch hẹn", compute='_compute_schedule_examine_count')
    count_special = fields.Integer(string="Special", compute='_compute_count_special', store=True)
    active = fields.Boolean(string="Active", default=True)

    @api.depends('special_customer_ids')
    def _compute_count_special(self):
        for line in self:
            line.count_special = len(line.special_customer_ids)

    def _compute_schedule_examine_count(self):
        schedule_examine = self.env['schedule_examine'].search([('sick_persion_id', 'in', self.ids)])
        # print(self.ids)
        # print(schedule_examine) == [13, 12, 11]
        # print(schedule_examine.id) ở đây không sai tại vì print(schedule_examine) == [13, 12, 11] là id của schedule_examine rồi
        for line in self:
            line.schedule_examine_count = len(schedule_examine.filtered(lambda f: f.sick_persion_id.id == line.id))
            print(self.ids)
            print(line.id)
            # print(schedule_examine.id)

    def action_open_schedule_examine(self):
        schedule_examine = self.env['schedule_examine'].search([('sick_persion_id', 'in', self.ids)])
        if not schedule_examine:
            return
        action = self.env.ref('hospital_management.action_schedule_examine_view').read()[0]
        domain = expression.AND([[], [('id', 'in', schedule_examine.ids)]])
        action['domain'] = domain
        return action

    def _compute_date(self):
        _examine_dates = self.env['examine_history_info'].search([('sick_persion_id', 'in', self.ids)])
        _re_examine_dates = self.env['schedule_examine'].search([('sick_persion_id', 'in', self.ids), ('state', '!=', 'cancel')])
        for line in self:
            examine_date = _examine_dates.filtered(lambda f: f.sick_persion_id.id == line.id)
            re_examine_date = _re_examine_dates.filtered(lambda f: f.sick_persion_id.id == line.id)
            line.examine_date = examine_date[0].examine_date if examine_date else False
            line.re_examine_date = re_examine_date[0].re_examine_date if re_examine_date else False

    def btn_create_special_customer(self):
        for line in self.filtered(lambda f: not f.special_customer_ids):
            self.env['special_customer'].create({
                'sick_persion_id': line.id,
            })

    @api.depends('birth_day')
    def _compute_age(self):
        for item in self:
            item.age = fields.Date.today().year - item.birth_day.year if item.birth_day else 0

    @api.depends('name', 'code', 'birth_day', 'phone')
    def _compute_name(self):
        for line in self:
            name_res = line.name + ' - ' + str(line.birth_day.strftime("%d/%m/%Y")) if line.birth_day else line.name
            name_res = name_res + ' - ' + line.phone if line.phone else name_res
            line.name_res = name_res

    def name_get(self):
        if not self._context.get('sick_persion', False):
            result = []
            for item in self:
                result.append((item.id, item.name))
            return result
        return super(SickPersionInfo, self).name_get()

    @api.model_create_multi
    def create(self, values):
        for i in range(0, len(values)):
            values[i]['code'] = self.env['ir.sequence'].next_by_code('sick_persion_code') or 'New'
            values[i]['name'] = values[i]['name'].upper()
        return super(SickPersionInfo, self).create(values)

    def write(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].upper()
        return super(SickPersionInfo, self.filtered(lambda f: f.company_id == f.env.company)).write(vals)

    def btn_add_examine_history(self):
        self.ensure_one()
        view_id = self.env.ref('hospital_management.examine_history_info_form_view')
        print(view_id.id, 1000)
        ctx = dict(
            default_sick_persion_id=self.id,
            default_medical_history=self.medical_history,
            default_allergy=self.allergy,
            default_heartbeat=self.heartbeat,
            default_blood_pressure=self.blood_pressure,
            default_eye_sight=self.eye_sight,
            default_height=self.height,
            default_weigh=self.weigh,
        )
        return {
            'name': 'Hồ sơ',
            'type': 'ir.actions.act_window',
            'res_model': 'examine_history_info',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': view_id.id,
            'target': 'inline',
            'context': ctx,
        }

    def btn_write_name(self):
        rec = self.search([])
        if self._context.get('return', False):
            for line in rec.filtered(lambda s: s.special_customer_ids):
                line.examine_history_ids.write({'special_customer_id': line.special_customer_ids[0].id})
            return
        for line in rec:
            line.write({'name': line.name})

    def action_create_schedule_examine(self):
        view_id = self.env.ref('hospital_management.schedule_examine_form_view_create')
        ctx = dict(self._context)
        ctx.update({
            'default_sick_persion_id': self.id,
            'default_type': '1',
            'default_is_create': False,
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

    def unlink(self):
        self.write({'active': False})
