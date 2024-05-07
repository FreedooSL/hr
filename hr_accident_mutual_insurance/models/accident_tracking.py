# -*- coding: utf-8 -*-
# © 2022 Soluciones Tecnológicas Freedoo: Stephany Zegarra Tejada <stephany@freedoo.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

class AccidentTracking(models.Model):
    _inherit = 'accident.tracking'

    def open_accident_wiz(self):
        report_with = self.env['ir.actions.report'].search([('report_name', '=', 'hr_accident_mutual_insurance.hr_employee_accident_unigemsa_report')], limit=1).id
        report_without = self.env['ir.actions.report'].search([('report_name', '=', 'hr_accident_mutual_insurance.hr_employee_accident_fremap_report')], limit=1).id
        if self.type_accident == 'with':
            report_id = report_with
        elif self.type_accident == 'without':
            report_id = report_without

        return {'type': 'ir.actions.act_window',
                'name': ('Imprimir informe de accidentes'),
                'res_model': 'accident.tracking.report.wiz',
                'target': 'new',
                'view_id': self.env.ref('hr_accident_mutual_insurance.open_accident_wiz_print_report_wizard').id,
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