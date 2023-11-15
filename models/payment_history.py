from odoo import api, fields, models


class PaymentHistory(models.Model):
    _name = 'payment_history'
    _inherit = ['private_data_company', 'mail.thread']
    _description = 'payment_history'
    _order = 'date desc'
    _rec_name = 'date'

    examine_line_id = fields.Many2one(comodel_name="examine_history_info", string="Phiếu khám", ondelete='cascade', required=True)
    sick_persion_id = fields.Many2one("sick_persion_info", string="Bệnh nhân", related='examine_line_id.sick_persion_id', store=True)
    address = fields.Char(string="Địa chỉ", related='sick_persion_id.address')
    date = fields.Date('Ngày thanh toán', default=fields.Date.today, required=True, tracking=True)
    amount = fields.Float("Số tiền", digits=(16, 0), tracking=True)
    doctor_id = fields.Many2one("doctor_info", string="Bác sĩ", required=True, tracking=True)
    currency_id = fields.Many2one('res.currency', string='Tiền tệ', default=lambda f: f.env.company.currency_id.id)
    active = fields.Boolean(string="Active", related='examine_line_id.active')
    payment_time = fields.Char('Thời gian thanh toán', compute='_compute_payment_time')

    def _compute_payment_time(self):
        for line in self:
            arrival_date = line.examine_line_id.examine_date
            pay_date = line.date
            diff = (pay_date - arrival_date).days
            if diff > 0:
                str_payment_time = f'Sau {diff} ngày'
            elif diff < 0:
                str_payment_time = f'Trước {abs(diff)} ngày'
            else:
                str_payment_time = 'Thanh toán ngay'
            line.payment_time = str_payment_time

    def btn_confirm(self):
        pass

    def unlink(self):
        for line in self:
            self.examine_line_id.write({
                'payment': self.examine_line_id.payment - line.amount,
                'debt': self.examine_line_id.debt + line.amount,
            })
        return super().unlink()

    def write(self, values):
        res = super().write(values)
        # res ở đây là True/False nên không truy cập được các trường
        for line in self.mapped('examine_line_id'):
            print(line, 1000)
            payment = sum(line.mapped('payment_history_ids.amount'))
            line.write({
                'payment': payment,
                'debt': line.amount - payment,
            })
        return res

    @api.model_create_multi
    def create(self, values):
        res = super().create(values)
        # res ở đây là 1 bản ghi còn self chỉ đại diện cho mô hình và chưa có giá trị gì
        for line in res.mapped('examine_line_id'):
            print(line, 100)
            payment = sum(line.mapped('payment_history_ids.amount'))
            # payment = sum(line.payment_history_ids.filtered(lambda ph: ph.create_date == res.create_date).mapped('amount'))

            print(line.mapped('payment_history_ids.amount'))
            line.write({
                'payment': payment,
                'debt': line.amount - payment,
            })
        return res
