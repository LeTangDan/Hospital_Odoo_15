from odoo import api, fields, models


class MedicineInfo(models.Model):
    _name = 'medicine_info'
    _inherit = ['private_data_company', 'delete_record']
    _rec_name = 'name_res'
    _description = 'Thông tin chi phí'
    _default_name = 'Xác nhận xóa Chi phí'
    _inactive = True

    name = fields.Char(u'Tên chi phí')
    code = fields.Char(string="Mã chi phí", copy=False)
    type = fields.Many2one(comodel_name="medicine_type", string="Loại", ondelete="restrict")
    user_manual = fields.Many2one(comodel_name="medicine_user_manual", string="Hướng dẫn sử dụng", ondelete='restrict')
    unit = fields.Many2one(comodel_name="medicine_unit", string="Đơn vị", ondelete='restrict')
    note = fields.Text(string="Ghi chú")
    price = fields.Float(string="Giá", digits=(16, 0))
    currency_id = fields.Many2one('res.currency', string='Tiền tệ', default=lambda f: f.env.company.currency_id.id)
    name_res = fields.Char(string="Name", compute='_compute_name', store=True)
    active = fields.Boolean(string="Active", default=True)

    _sql_constraints = [('code_uniq', 'unique(code, company_id)', 'Mã chi phí đã tồn tại!')]

    @api.depends('name', 'code')
    def _compute_name(self):
        for line in self:
            line.name_res = '[' + line.code + '] ' + line.name

    def name_get(self):
        return super(MedicineInfo, self).name_get()


class MedicineInfoLine(models.Model):
    _name = 'medicine_info_line'
    _rec_name = 'medicine_id'
    _description = 'Thông tin chi phí'

    medicine_id = fields.Many2one(comodel_name="medicine_info", string="Tên chi phí", ondelete='restrict')
    type = fields.Char(string="Loại", related='medicine_id.type.name', store=True)
    user_manual = fields.Char(string="HD sử dụng")
    unit = fields.Many2one(comodel_name="medicine_unit", string="Đơn vị", required=1, ondelete='restrict')
    note = fields.Text(string="Ghi chú", related='medicine_id.note', store=True)
    price = fields.Float(string="Giá", required=1, digits=(16, 0))
    quantity = fields.Integer(string="Số lượng", default=1, required=1)
    examine_line_id = fields.Many2one(comodel_name="examine_history_info", string="Hồ sơ thăm khám", ondelete='cascade')
    amount = fields.Float(string="Tổng", digits=(16, 0))
    currency_id = fields.Many2one('res.currency', string='Tiền tệ', default=lambda f: f.env.company.currency_id.id)

    @api.onchange('quantity')
    def onchange_quantity(self):
        self.amount = self.price * self.quantity

    @api.onchange('price')
    def onchange_price(self):
        self.amount = self.price * self.quantity

    @api.onchange('medicine_id')
    def onchange_medicine_id(self):
        if self.medicine_id:
            self.quantity = 1
            self.unit = self.medicine_id.unit.id
            self.user_manual = self.medicine_id.user_manual.name
            self.price = self.medicine_id.price
            self.amount = self.price * self.quantity
