# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class SallaIntegration(http.Controller):
    @http.route('/code', auth='public')
    def index(self, **kw):
        auth_code = kw['code']
        c_user = request.env['res.users'].search([('id', '=', request.env.context['uid'])])
        c_user.salla_code = auth_code
