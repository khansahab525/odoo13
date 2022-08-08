# -*- coding: utf-8 -*-
from datetime import datetime, date

import requests
from requests.structures import CaseInsensitiveDict

from odoo import models, fields, api, _


class SallaIntegration(models.Model):
    _name = 'salla.integration'
    _description = 'salla_integration'

    con_url = fields.Char(string='URL', compute='generate_url_link')
    token_key = fields.Char(required=True)
    endponts = fields.Selection(
        [('orders', 'List Orders'), ('customers', 'List Customers'), ('products', 'List Products')], required=True,
        default='orders')
    page_from = fields.Integer(required=True)
    page_to = fields.Integer(required=True)
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)

    @api.depends('endponts')
    def generate_url_link(self):
        for record in self:
            common_url = "https://api.salla.dev/admin/v2/"
            record.con_url = common_url + record.endponts

    def salla_connection(self,data):
        url = self.con_url+"?page="+f"{data}"
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer"+" "+self.token_key
        resp = requests.get(url, headers=headers)
        json_object = resp.json()
        return json_object


    def salla_integration_orders(self):
        start_page = self.page_from
        end_page = self.page_to
        # date = self.date_from-self.date_to
        while start_page<=end_page:
            connection_login = self.salla_connection(data=start_page)
            for i in connection_login.get('data'):
                date = i.get('date').get('date').split(".")[0]
                created_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date()
                if created_date>=self.date_from and created_date<=self.date_to:
                    status = i.get('status')
                    customer_name = status.get('name')
                    partner_record = self.env['res.partner'].sudo()
                    search_record = partner_record.search([('name', '=', customer_name)])
                    if not search_record:
                        partner_record.create({
                            'name': customer_name,
                            'city': 'الرياض'
                        })
                        self.env.cr.commit()

                    new_id = partner_record.id
                    if not new_id:
                        new_id = search_record.id
                    new_vals = {
                        'partner_id': new_id,
                        'date_order':created_date,
                        'create_date':created_date

                    }
                    sale_order_id = self.env['sale.order'].sudo().create(new_vals)

                    """"sale order_line portion"""
                    try:
                        items = i.get('items')
                        for item in items:
                            search_product = self.env['product.template'].search([('name', '=', item.get('name'))])
                            vall_record = search_product.ids[0]
                            error_list = []
                            if not search_product:
                                error_list.append(sale_order_id)
                                print(error_list)
                            else:
                                order_line_vals = {
                                    'product_id': vall_record,
                                    'order_id': sale_order_id.id
                                }
                                sale_order_line = self.env['sale.order.line'].create(order_line_vals)
                    except:
                        continue

                else:
                    pass

            current_page_no = connection_login.get('pagination').get('links').get('next')[-1]
            start_page+=1



        hh = 9

    def salla_integration_products(self):
        pass

    def salla_integration_customers(self):
        pass


class SallaInherit(models.Model):
    _inherit = 'sale.order'

    create_date = fields.Date(readonly=True, related='date_order')
    date_order = fields.Date(readonly=True)



    # def salla_connection(self):
    #     url = "https://api.salla.dev/admin/v2/orders"
    #     headers = CaseInsensitiveDict()
    #     headers["Accept"] = "application/json"
    #     headers["Authorization"] = "Bearer 822066500c927bbf8564d0e64360e9c9ba8eba5e35f1d04ce599b4efd3f48518cd85068792"
    #
    #     resp = requests.get(url, headers=headers)
    #     d = resp.json()
    #     for i in d.get('data'):
    #         status = i.get('status')
    #
    #         customer_name = status.get('name')
    #         partner_record = self.env['res.partner'].sudo()
    #         search_record = partner_record.search([('name', '=', customer_name)])
    #         if not search_record:
    #             partner_record.create({'name': customer_name})
    #             self.env.cr.commit()
    #
    #         new_id = partner_record.id
    #         if not new_id:
    #             new_id = search_record.id
    #         new_vals = {
    #             'partner_id': new_id
    #         }
    #         sale_order_id = self.env['sale.order'].sudo().create(new_vals)
    #
    #         """"sale order_line portion"""
    #         try:
    #
    #             items = i.get('items')
    #             for item in items:
    #                 search_product = self.env['product.template'].search([('name', '=', item.get('name'))])
    #                 vall_record = search_product.ids[0]
    #
    #                 if not search_product:
    #                     pass
    #                 else:
    #                     order_line_vals = {
    #                         'product_id': vall_record,
    #                         'order_id': sale_order_id.id
    #                     }
    #                     sale_order_line = self.env['sale.order.line'].create(order_line_vals)
    #                     break
    #         except:
    #             continue


class NewModule(models.Model):
    _inherit = 'res.partner'

    salla_contacts_id = fields.Integer('Id')

    def salla_contacts(self):
        url = "https://api.salla.dev/admin/v2/customers"
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer 822066500c927bbf8564d0e64360e9c9ba8eba5e35f1d04ce599b4efd3f48518cd85068792"

        resp = requests.get(url, headers=headers)
        d = resp.json()
        names_list = []
        for i in d.get('data'):
            vals = {
                'salla_contacts_id': i.get('id'),
                'name': i.get('first_name'),
                'mobile': i.get('mobile'),
                'email': i.get('email'),
                'city': i.get('city'),
                'street': i.get('location')
            }

            names_list.append(i.get('first_name'))
            partner_record = self.env['res.partner'].sudo()
            search_record = partner_record.search([('name', '=', i.get('first_name'))])
            if not search_record:
                partner_record.create(vals)
                self.env.cr.commit()
            else:
                pass

    def salla_product(self):
        pass
    #     g = 7
    #     url = "https://api.salla.dev/admin/v2/products"
    #     headers = CaseInsensitiveDict()
    #     headers["Accept"] = "application/json"
    #     headers["Authorization"] = "Bearer 822066500c927bbf8564d0e64360e9c9ba8eba5e35f1d04ce599b4efd3f48518cd85068792"
    #
    #     resp = requests.get(url, headers=headers)
    #     d = resp.json()
    #     names_list = []
    #     for i in d.get('data'):
    #         vals = {
    #             'name': i.get('name'),
    #             'type': i.get('type'),
    #             'lst_price': i['price']['amount'],
    #             'default_code': i.get('id')
    #         }
    #         names_list.append(i.get('name'))
    #         partner_record = self.env['product.product'].sudo()
    #         search_record = partner_record.search([('name', '=', i.get('name'))])
    #         if not search_record:
    #             partner_record.create(vals)
    #             self.env.cr.commit()
    #         else:
    #             pass
