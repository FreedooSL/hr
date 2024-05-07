# -*- coding: utf-8 -*-
# © 2022 Soluciones Tecnológicas Freedoo: Stephany Zegarra Tejada <stephany@freedoo.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api
from odoo.exceptions import ValidationError
import datetime
import base64

class AccidentTrackingReport(models.Model):
    _name = 'accident.tracking.report'
    _description = 'Accident tracking report'

    name = fields.Char(string="Name")
    attachment = fields.Binary(string="Download", related="attachment_id.datas")
    create_uid_attach = fields.Many2one(string="Create User", related="attachment_id.create_uid")
    create_date_attach = fields.Datetime(string="Create Date", related="attachment_id.create_date")
    attachment_id = fields.Many2one(comodel_name="ir.attachment")
    accident_id = fields.Many2one(string="Report", comodel_name="accident.tracking")
    

class AccidentTracking(models.Model):
    _name = 'accident.tracking'
    _description = 'Accident tracking for employee'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", default="Nuevo registro")
    employee_id = fields.Many2one(string="Employee", comodel_name="hr.employee")
    type_accident = fields.Selection(string="The accident is ...",
                                     selection=[('with', 'Accident with sick leave'),
                                                ('without', 'Accident without sick leave')])
    tracking_report_ids = fields.One2many(string="Tracking of reports",
                                          comodel_name="accident.tracking.report",
                                          inverse_name="accident_id")
    state = fields.Selection(selection=[('draft', 'Draft'),
                                        ('confirmed', 'Confirmed')], default='draft')
    attachment_number = fields.Integer(compute='_compute_attachment_number', string='Number of Attachments')

    #ACCIDENTE CON BAJA
    datetime_accident = fields.Datetime(string="Date of accident")
    date_leave = fields.Date(string="Leaving date")
    work_hours = fields.Char(string="Work Schedule")
    description = fields.Text(string="Description")
    type_work = fields.Text(string="Type Work")
    doing = fields.Text(string="What specifically were you doing at the time of the accident?")
    abnormal = fields.Text(string="What abnormal event that deviates from the deviating from the usual process, triggered the accident?")
    how = fields.Text(string="How was the injured person injured?")
    description_lesion = fields.Text(string="Description of injury")
    type_location = fields.Text(string="What kind of location was it in?")
    bool_company = fields.Boolean(string="Did it happen in the company?")
    name_location = fields.Char(string="Company name")
    cif_location = fields.Char(string="Cif Company")
    eco_activity_location = fields.Char(string="Economic Activity")
    address_location = fields.Char(string="Address")
    phone_location = fields.Char(string="Phone")
    staff = fields.Char(string="Staff")
    #ACCIDENTE SIN BAJA
    date_accident = fields.Date(string="Date of accident")
    hour_accident = fields.Float(string="Hour of accident")
    description_accident = fields.Text(string="Description")

    @api.model
    def create(self, vals):
        res = super(AccidentTracking, self).create(vals)
        for rec in res:
            reg = self.search_count([]) + 1
            year = datetime.date.today().strftime("%Y")
            if rec.employee_id.name:
                rec.name = rec.employee_id.name + '/' + year + '/' + str(reg)
        return res


    def validate_field_length(self, field, value):
        if value and len(value) < 20:
            raise ValidationError('El campo [' + self.env['accident.tracking']._fields[field].string + '] tiene menos de 20 caracteres')

    @api.constrains('description', 'doing', 'abnormal', 'how', 'description_lesion', 'description_accident')
    def control_min_charac(self):
        self.validate_field_length('description', self.description)
        self.validate_field_length('doing', self.doing)
        self.validate_field_length('abnormal', self.abnormal)
        self.validate_field_length('how', self.how)
        self.validate_field_length('description_lesion', self.description_lesion)
        self.validate_field_length('description', self.description)

    def open_accident_wiz(self):
        report_with = self.env['ir.actions.report'].search([('activate_accident_with_or_without', '=', 'with')], limit=1).id
        report_without = self.env['ir.actions.report'].search([('activate_accident_with_or_without', '=', 'without')], limit=1).id
        if self.type_accident == 'with':
            report_id = report_with
        elif self.type_accident == 'without':
            report_id = report_without

        return {'type': 'ir.actions.act_window',
                'name': ('Imprimir informe de accidentes'),
                'res_model': 'accident.tracking.report.wiz',
                'target': 'new',
                'view_id': self.env.ref('accident_report_tracking.open_accident_wiz_print_report_wizard').id,
                'view_mode': 'form',
                'context': {
                        'default_type_accident': self.type_accident,
                        'default_accident_id': self.id,
                        'default_report_id': report_id,
                    }
                }
    
    def _compute_attachment_number(self):
        attachment_data = self.env['ir.attachment'].read_group([('res_model', '=', 'accident.tracking'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for accident in self:
            accident.attachment_number = attachment.get(accident.id, 0)
        if self.attachment_number > 0:
            self.state = 'confirmed'
    
    def action_get_attachment_view(self):
        self.ensure_one()
        res = self.env['ir.actions.act_window']._for_xml_id('base.action_attachment')
        res['domain'] = [('res_model', '=', 'accident.tracking'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'accident.tracking', 'default_res_id': self.id}
        return res