from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    specialize = fields.Char(string="Chuyên khoa")
    hotline = fields.Char(string="Hotline")
    note_x = fields.Char(string="Lời cảm ơn")
    payment_info = fields.Text(string="Thông tin thanh toán")

    def btn_company_info(self):
        view_id = self.env.ref('hospital_management.res_company_form_inherit_view')
        company = self._context.get('allowed_company_ids') and self._context.get('allowed_company_ids')[0] or self.env.user.company_id.id
        return {
            'name': 'Thông tin phòng khám',
            'type': 'ir.actions.act_window',
            'res_model': 'res.company',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': view_id.id,
            'target': 'new',
            'res_id': company,
        }


class Partner(models.Model):
    _inherit = 'res.partner'


class ReportPaperformat(models.Model):
    _inherit = 'report.paperformat'

    def btn_report_paperformat_edit(self):
        res_id = self.env.ref('hospital_management.paperformat_custom')
        return {
            'name': 'Định dạng phiếu in',
            'type': 'ir.actions.act_window',
            'res_model': 'report.paperformat',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'res_id': res_id.id,
        }
