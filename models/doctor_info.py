from odoo import api, fields, models, _
from . import lib_default_avatar


_birth = []
for item in range(fields.Date.today().year - 80, fields.Date.today().year):
    _bir = (str(item), item)
    _birth.append(_bir)

_exper = []
for exp in range(0, 100):
    _exp = (str(exp), exp)
    _exper.append(_exp)


class DoctorInfo(models.Model):
    _name = 'doctor_info'
    _inherit = ['private_data_company']
    _rec_name = 'name'
    _description = 'Bác sĩ'

    avatar = fields.Binary(string="Ảnh đại diện", attachment=True, default=lib_default_avatar._default_image())
    name = fields.Char(string='Họ tên', copy=False)
    code = fields.Char(string="Mã số", readonly=True, default='New')
    birth = fields.Selection(string="Năm sinh", selection=_birth)
    degree = fields.Char(string='Học vị/cấp bậc')
    position = fields.Char(string='Chức vụ')
    major = fields.Char(string='Chuyên khoa')
    phone = fields.Char(string='Điện thoại')
    mail = fields.Char(string='Mail')
    address = fields.Char(string='Địa chỉ')
    exper = fields.Selection(string='Số năm kinh nghiệm', selection=_exper)

    _sql_constraints = [('name', 'unique(name, company_id)', 'Tên đã tồn tại!')]

    def name_get(self):
        return super(DoctorInfo, self).name_get()

    @api.model_create_multi
    def create(self, values):
        for i in range(0, len(values)):
            values[i]['code'] = self.env['ir.sequence'].next_by_code('doctor_info_code') or 'New'
        res = super(DoctorInfo, self).create(values)
        return res
