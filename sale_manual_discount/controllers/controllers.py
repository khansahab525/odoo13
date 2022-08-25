# # -*- coding: utf-8 -*-
# from odoo import http
#
# class SaleManualDiscount(http.Controller):
#     @http.route('/', type='http', auth="public", website=True)
#     def index(self, s_action=None, db=None, **kw):
#         print('hellllllllllllll')
#         return 'hello'


# -- coding: utf-8 --
import string
from collections import defaultdict
from odoo import http
from odoo.http import request


class MediHomes(http.Controller):
    @http.route('/', type='http', auth='public', website=True)
    def Home(self, **kw):
        products = request.env['product.product'].search([])
        return request.render('website.homepage', {'products': products})

    @http.route(['/test/product'], type='http', auth='public', website=True)
    def new_acc(self, redirect=None, **vals):
        t =6
        return f"{vals}"
        # request.redirect('/my/home')
