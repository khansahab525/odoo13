from odoo import http, models
from odoo.http import request


from odoo.http import request
import json

# $$$$$$$$$$$$$$    MAST CONNECTOR AUTHENTICATION    &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class MastBeautyConnectorController(http.Controller):
    @http.route('/web/session/authenticate', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        session_details = request.env['ir.http'].session_info()
        return session_details

    @http.route('/web/get/contacts', type='json', auth='user')
    def get_contacts(self):
        student_rec = request.env['res.partner'].search([])
        std_list = []
        for rec in student_rec:
            std_dic = {
                'id': rec.id,
                'name': rec.name,
                'email': rec.email,

            }
            std_list.append(std_dic)

        return std_list
    #
