from odoo import api, fields, models


class ConfirmMsgUnlink(models.TransientModel):
    _name = 'confirm_msg_unlink'
    _description = 'Confirm Msg Unlink'

    name = fields.Char(string="Confirm")

    def btn_unlink(self):
        _model = self.env.context.get('active_model', False)
        _id = self.env.context.get('active_id', False)
        if _model and _id:
            self.env[_model].search([('id', '=', _id)], limit=1).with_context(inactive=self._context.get('inactive', False)).unlink()
        return {'type': 'ir.actions.act_window_close'}
