# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ActiveField(models.AbstractModel):
    _name = 'active_field'
    _description = 'Active Field'

    active = fields.Boolean(string="Active", default=True)

    def write(self, values):
        result = super(ActiveField, self.filtered(lambda f: f.create_uid == f.env.user)).write(values)
        return result


class MedicineUnit(models.Model):
    _name = 'medicine_unit'
    _rec_name = 'name'
    _description = 'Medicine Unit'
    _inherit = ['delete_record', 'active_field']
    _default_name = 'Xác nhận xóa Đơn vị tính'
    _inactive = True

    name = fields.Char(string="Tên đơn vị", copy=False)

    _sql_constraints = [('name_uniq', 'unique(name)', 'Tên đơn vị đã tồn tại!')]


class MedicineType(models.Model):
    _name = 'medicine_type'
    _rec_name = 'name'
    _description = 'Medicine Type'
    _inherit = ['delete_record', 'active_field']
    _default_name = 'Xác nhận xóa Loại chi phí'
    _inactive = True

    name = fields.Char(string="Loại chi phí", copy=False)

    _sql_constraints = [('name_uniq', 'unique(name)', 'Loại chi phí đã tồn tại!')]


class MedicineUserManual(models.Model):
    _name = 'medicine_user_manual'
    _rec_name = 'name'
    _description = 'Medicine User Manual'
    _inherit = ['delete_record', 'active_field']
    _default_name = 'Xác nhận xóa Hướng dẫn sử dụng'
    _inactive = True

    name = fields.Char(string="Hướng dẫn sử dụng", copy=False)

    _sql_constraints = [('name_uniq', 'unique(name)', 'Hướng dẫn sử dụng đã tồn tại!')]


class CustomerType(models.Model):
    _name = 'customer_type'
    _rec_name = 'name'
    _description = 'Customer Type'
    _inherit = ['delete_record', 'active_field']
    _default_name = 'Xác nhận xóa Loại bệnh nhân'
    _inactive = True

    name = fields.Char(string="Loại", copy=False)

    _sql_constraints = [('name_uniq', 'unique(name)', 'Tên loại đã tồn tại!')]


