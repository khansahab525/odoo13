# -*- coding: utf-8 -*-
import requests
from random import randint
from odoo import models, fields, api, _
from datetime import datetime


# # &&&&&&& INHERIT CAMPUS TO ADD MOODLE REQUIRED FIELDS &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class InheritIacCampus(models.Model):
    _inherit = 'odoocms.campus'

    # campus_moodle_id = fields.Char(string='Moodle ID')
    iac_moodle_id = fields.Char(string='Moodle ID')
    # moodle_city_id = fields.Many2one('odoocms.city', string='City')
    # disp_moodle_id_on_campus = fields.Char()
    # sync_state = fields.Selection([('sync', 'Sync'), ('not_sync', 'Unsync')], default='not_sync')
    iac_sync_state = fields.Selection([('sync', 'Sync'), ('not_sync', 'Unsync')], default='not_sync')

    def sync_campus_to_moodle(self):
        if self.env.user.iac_access_token is False or self.env.user.iac_url is False:
            raise models.ValidationError("You are not login to moodle. Plz check it")
        for record in self:
            if record.iac_moodle_id is False:
                url = self.env.user.iac_url
                data = {
                    'wstoken': self.env.user.iac_access_token,
                    'wsfunction': 'core_course_create_categories',
                    'moodlewsrestformat': 'json', }
                data['categories[0][parent]'] = '0'
                data['categories[0][name]'] = record.name
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                try:
                    request_data = requests.post(url=url, params=data, headers=headers)
                    record.iac_moodle_id = str(request_data.json()[0].get('id'))
                    record.iac_sync_state = 'sync'
                except Exception as e:
                    raise models.ValidationError(
                        f"Something went wrong for ID {record.id}, {e}")


# # &&&&&&& INHERIT CAMPUS TO ADD MOODLE REQUIRED FIELDS &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class InheritIacSchool(models.Model):
    _inherit = 'odoocms.institute'

    iac_moodle_id = fields.Char(string='Moodle ID')
    iac_sync_state = fields.Selection([('sync', 'Sync'), ('not_sync', 'Unsync')], default='not_sync')

    def sync_institute_to_moodle(self):
        if self.env.user.iac_access_token is False or self.env.user.iac_url is False:
            raise models.ValidationError("You are not login to moodle. Plz check it")
        for record in self:
            if record.iac_moodle_id is False:
                url = self.env.user.iac_url
                data = {
                    'wstoken': self.env.user.iac_access_token,
                    'wsfunction': 'core_course_create_categories',
                    'moodlewsrestformat': 'json', }
                data['categories[0][parent]'] = record.campus_id.iac_moodle_id
                data['categories[0][name]'] = record.name
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                try:
                    request_data = requests.post(url=url, params=data, headers=headers)
                    record.iac_moodle_id = str(request_data.json()[0].get('id'))
                    record.iac_sync_state = 'sync'
                except Exception as e:
                    raise models.ValidationError(
                        f"Something went wrong for ID {record.id}, {e}")


class InheritIacDepartment(models.Model):
    _inherit = 'odoocms.department'

    iac_moodle_id = fields.Char(string='Moodle ID')
    iac_sync_state = fields.Selection([('sync', 'Sync'), ('not_sync', 'Unsync')], default='not_sync')

    def sync_department_to_moodle(self):
        if self.env.user.iac_access_token is False or self.env.user.iac_url is False:
            raise models.ValidationError("You are not login to moodle. Plz check it")
        for record in self:
            if record.iac_moodle_id is False:
                url = self.env.user.iac_url
                data = {
                    'wstoken': self.env.user.iac_access_token,
                    'wsfunction': 'core_course_create_categories',
                    'moodlewsrestformat': 'json', }
                data['categories[0][parent]'] = record.institute_id.iac_moodle_id
                data['categories[0][name]'] = record.name
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                try:
                    request_data = requests.post(url=url, params=data, headers=headers)
                    record.iac_moodle_id = str(request_data.json()[0].get('id'))
                    record.iac_sync_state = 'sync'
                except Exception as e:
                    raise models.ValidationError(
                        f"Something went wrong for ID {record.id}, {e}")


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& INHERIT PROGRAM  &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
class InheritiACAcademicProgram(models.Model):
    _inherit = 'odoocms.program'

    iac_moodle_id = fields.Char(string='Moodle ID')
    iac_sync_state = fields.Selection([('sync', 'Sync'), ('not_sync', 'Unsync')], default='not_sync')

    def sync_program_to_moodle(self):
        if self.env.user.iac_access_token is False or self.env.user.iac_url is False:
            raise models.ValidationError("You are not login to moodle. Plz check it")
        for record in self:
            if record.iac_moodle_id is False:
                url = self.env.user.iac_url
                data = {
                    'wstoken': self.env.user.iac_access_token,
                    'wsfunction': 'core_course_create_categories',
                    'moodlewsrestformat': 'json', }
                data['categories[0][parent]'] = record.department_id.iac_moodle_id
                data['categories[0][name]'] = record.name
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                try:
                    request_data = requests.post(url=url, params=data, headers=headers)
                    record.iac_moodle_id = str(request_data.json()[0].get('id'))
                    record.iac_sync_state = 'sync'
                except Exception as e:
                    raise models.ValidationError(
                        f"Something went wrong for ID {record.id}, {e}")
