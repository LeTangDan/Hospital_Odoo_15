from odoo import api, fields, models
from odoo.osv import expression


class PrivateDataCompany(models.AbstractModel):
    _name = 'private_data_company'
    _description = 'private data company'

    company_id = fields.Many2one(comodel_name="res.company", string="Company", required=True, default=lambda x: x.env.company)

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        args = expression.AND([args, [('company_id', '=', self.env.company.id)]])
        return super(PrivateDataCompany, self)._search(args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        domain = expression.AND([domain, [('company_id', '=', self.env.company.id)]])
        return super(PrivateDataCompany, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)

    def write(self, values):
        result = super(PrivateDataCompany, self.filtered(lambda f: f.company_id == f.env.company)).write(values)
        return result


class DeleteRecord(models.AbstractModel):
    _name = 'delete_record'
    _description = 'Delete Record'
    _default_name = 'Delete'
    _inactive = False

    def btn_confirm_unlink(self):
        view_id = self.env.ref('hospital_management.confirm_msg_unlink_form_view')
        ctx = dict(
            default_name=self._default_name,
            inactive=self._inactive,
        )
        return {
            'name': 'Xác nhận',
            'type': 'ir.actions.act_window',
            'res_model': 'confirm_msg_unlink',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': view_id.id,
            'target': 'new',
            'res_id': False,
            'context': ctx,
        }

    def unlink(self):
        if self._context.get('inactive', False):
            self.write({'active': False})
        else:
            return super(DeleteRecord, self).unlink()



