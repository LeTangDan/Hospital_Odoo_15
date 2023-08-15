from odoo import api, fields, models


class PotentialPatient(models.Model):
    _name = 'potential_patient'
    _inherit = ['private_data_company', 'delete_record']
    _rec_name = 'sick_persion_id'
    _order = 'id desc'
    _description = 'Bệnh nhân tiềm năng'
    _default_name = 'Xác nhận xóa bệnh nhân tiềm năng'
    _inactive = False

    sick_persion_id = fields.Many2one(comodel_name="sick_persion_info", string="Bệnh nhân", required=True)
    tinh_trang = fields.Char('Tình trạng')
    ly_do = fields.Char('Lý do sẽ quay lại')
