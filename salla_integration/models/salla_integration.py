from odoo import models, fields, api, _
import requests
from odoo.exceptions import UserError
import time

HEADER = {'Content-type': 'Application/Json'}


class ResConfigSettings(models.Model):
    _inherit = "res.users"

    salla_code = fields.Char("Salla Code")
    salla_access_token = fields.Char("Access Token")
    salla_refresh_token = fields.Char("Refresh Token")
    token_expire_in = fields.Char("Expire In")


class SallaIntegrationModel(models.Model):
    _name = 'salla.settings'
    _description = "Salla Module setting"
    _rec_name = 'email'

    store_id = fields.Many2one('salla.stores', 'Store')
    email = fields.Char("Email", required=True)
    password = fields.Char("Password", required=True)
    client_id = fields.Char("Client Id", required=True)
    client_secret = fields.Char("Client Secret", required=True)
    your_url = fields.Char("Your URL", required=True, help='e.g. http://example.com')
    redirect_url = fields.Char("Redirect URL", help='You must place that url in your salla call back url also')
    login_url = fields.Char("Access URL", readonly=True)
    code = fields.Char('Code', readonly=True)
    access_token = fields.Char('Access Token', readonly=True)
    status = fields.Selection([
        ('ready', 'Ready'), ('fail', 'Fail'), ('successful', 'Successful')
    ], default='ready')

    # prepare redirect and access url to get code
    def prepare_url(self):
        for rec in self:
            # first set redirect url
            rec.redirect_url = self.your_url + '/code' if rec.your_url else self.message_wizard("Your url Not Set",
                                                                                                'Your URL Not Set '
                                                                                                'please provide a '
                                                                                                'valid URL')

            # second set access url
            authorize_url = "https://accounts.salla.sa/oauth2/auth"
            redirect_url = 'redirect_uri=' + str(rec.redirect_url) + '&'
            client_id = 'client_id=' + str(rec.client_id) + '&'
            authorize_url = str(authorize_url) + '?'
            scope = "offline_access"
            rec.login_url = authorize_url + redirect_url + client_id + 'response_type=code&' + 'state=12345678&' + scope
            response = requests.post(self.login_url, headers=HEADER)

            if response.status_code in [200, 201]:
                message = 'Your URL has been settled successfully Now You can Get Access by clicking the access button'
                return self.message_wizard('Success', message)
            else:
                message = 'You have some problem in your details please check your details'
                return self.message_wizard('Failure', message)

    # to get the code for access token
    def get_access(self):
        for rec in self:
            if not rec.login_url or not rec.redirect_url:
                raise UserError(_("Please Click Generate Redirect and Access Url Button"))
            else:
                response = requests.post(self.login_url, headers=HEADER)
                if response.status_code in [200, 201]:
                    return {'type': 'ir.actions.act_url',
                            'url': self.login_url,
                            'target': 'new',
                            'res_id': self.id,
                            }
                else:
                    raise UserError(_("Your Login Url is Not set correctly please Review your details"))

    def get_token(self):
        for rec in self:
            rec.code = self.env.user.salla_code
            if not rec.code:
                raise UserError(
                    _("You have some problem in your Credentials Please fill all the details carefully and click on "
                      "generate redirect and access url button and then get access button and after all of this click "
                      "on connect button"))
            else:
                header = {'Content-Type': 'application/x-www-form-urlencoded'}
                response = requests.post("https://accounts.salla.sa/oauth2/token?",
                                         data='grant_type=authorization_code&code=' + rec.code + '&redirect_uri='
                                              + rec.redirect_url + '&client_id=' + rec.client_id + '&client_secret='
                                              + rec.client_secret + '&state=12345678&offline_access',
                                         headers=header)
                if response.status_code in [200, 201]:
                    self.env.user.salla_access_token = response.json()['access_token']
                    rec.access_token = response.json()['access_token']
                    # self.env.user.salla_refresh_token = response['refresh_token']
                    # self.env.token_expire_in = int(round(time.time() * 1000))
                    # self.env.user.expire_in = self.expire_in
                    self.status = 'successful'
                    return self.message_wizard("Connected", 'Connected Successfully to salla store')
                elif response.status_code == 400:
                    return self.message_wizard("Code Used",
                                               'You have already used the code click get access button to get the new '
                                               'code')
                else:
                    return self.message_wizard('Fail', 'No connected Please Check your details Carefully')

    # To popup desired message on the screen
    def message_wizard(self, name=None, message=None):
        created_id = self.env['wk.wizard.message'].create({
            'text': (_(message))
        })
        return {
            'name': (_(name)),
            'type': 'ir.actions.act_window',
            'res_model': 'wk.wizard.message',
            'view_mode': 'form',
            'target': 'new',
            'res_id': created_id.id,
        }
