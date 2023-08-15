from odoo import api, fields, models


class SpecialCustomer(models.Model):
    _name = 'special_customer'
    _rec_name = 'sick_persion_id'
    _description = 'Bệnh nhân đặc biệt'
    _inherit = ['mail.thread', 'private_data_company']
    _order = 'id desc'

    sick_persion_id = fields.Many2one(comodel_name="sick_persion_info", string="Bệnh nhân", ondelete="restrict", required=True)
    avatar = fields.Binary(string="Ảnh đại diện", attachment=True, related='sick_persion_id.avatar')
    birth_day = fields.Date(string="Ngày sinh", related='sick_persion_id.birth_day')
    phone = fields.Char(string="Điện thoại", related='sick_persion_id.phone')
    customer_type_id = fields.Many2one(comodel_name="customer_type", string="Loại bệnh nhân", related='sick_persion_id.customer_type_id', store=True)
    examine_history_ids = fields.One2many(comodel_name="examine_history_info", inverse_name="special_customer_id", string="Hồ sơ thăm khám", required=False)
