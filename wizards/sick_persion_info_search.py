from odoo import api, fields, models
from datetime import datetime
from calendar import monthrange
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval

CHOICE = [
    ('tc', 'tất cả'),
    ('tk', 'trong khoảng'),
    ('b', 'bằng'),
    ('kb', 'không bằng'),
    ('s', 'sau'),
    ('t', 'trước'),
    ('sb', 'sau hoặc bằng'),
    ('tb', 'trước hoặc bằng')
]


class SickPersionInfoSearch(models.TransientModel):
    _name = 'sick_persion_info_search'
    _description = 'Sick Perasion Info Search'
    _rec_name = 'name'

    def _get_default_from_date(self):
        _date = datetime.now()
        start_date = datetime.strptime('01/{:02d}/{:04d}'.format(_date.month, _date.year), '%d/%m/%Y')
        return start_date

    def _get_default_to_date(self):
        _date = datetime.now()
        last_day_of_month = monthrange(_date.year, _date.month)[1]
        end_date = datetime.strptime('{:02d}/{:02d}/{:04d}'.format(last_day_of_month, _date.month, _date.year), '%d/%m/%Y')
        return end_date

    name = fields.Char(string="Name", default='.')
    from_date = fields.Date(string="Từ ngày", default=_get_default_from_date)
    to_date = fields.Date(string="Đến ngày", default=_get_default_to_date)
    customer_ids = fields.Many2many('sick_persion_info', 'sick_persion_info_m2m_rel', 'search_id', 'customer_id', 'Bệnh nhân')
    doctor_ids = fields.Many2many('doctor_info', 'doctor_info_m2m_rel', 'search_id', 'doctor_id', 'Bác sĩ')
    state = fields.Selection(string="Ngày khám", selection=CHOICE, required=True, default='tc')

    def btn_search(self):
        action = self.env.ref(self._context.get('view_action')).read()[0]
        domain = safe_eval(action['domain'])
        date = self._context.get('date')
        if self.state == 'tk':
            domain = expression.AND([domain, [(date, '>=', self.from_date)]])
            domain = expression.AND([domain, [(date, '<=', self.to_date)]])
        elif self.state == 'b':
            domain = expression.AND([domain, [(date, '=', self.from_date)]])
        elif self.state == 'kb':
            domain = expression.AND([domain, [(date, '!=', self.from_date)]])
        elif self.state == 's':
            domain = expression.AND([domain, [(date, '>', self.from_date)]])
        elif self.state == 't':
            domain = expression.AND([domain, [(date, '<', self.from_date)]])
        elif self.state == 'sb':
            domain = expression.AND([domain, [(date, '>=', self.from_date)]])
        elif self.state == 'tb':
            domain = expression.AND([domain, [(date, '<=', self.from_date)]])
        if self.customer_ids:
            domain = expression.AND([domain, [('sick_persion_id', 'in', self.customer_ids.ids)]])
        if self.doctor_ids:
            domain = expression.AND([domain, [('doctor_id', 'in', self.doctor_ids.ids)]])
        action['domain'] = domain
        return action
