# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleDiscountInheritSale(models.Model):
    _inherit = 'sale.order'

    manual_discount_type = fields.Selection(
        [('manual_disc', 'Manual Discount'), ('percentage_disc', 'Percentage Discount')],
        string='Manual Discount')
    manual_discount = fields.Float()

    def _prepare_invoice(self):
        res = super(SaleDiscountInheritSale, self)._prepare_invoice()
        trade_account = self.env.ref('l10n_generic_coa.1_expense').id
        so_line = self.order_line
        line = {
            'account_id': trade_account,
            'name': 'Discount Offer',
            'price_unit': self.manual_discount,
            # 'price_unit': res['less_trade_offer'],
            'exclude_from_invoice_tab': True,
            'quantity' : -1.0
        }
        res['invoice_line_ids'].append(line)
        return res
