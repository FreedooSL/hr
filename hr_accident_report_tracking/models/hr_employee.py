# -*- coding: utf-8 -*-
# © 2022 Soluciones Tecnológicas Freedoo: Stephany Zegarra Tejada <stephany@freedoo.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    accident_count = fields.Integer(compute="compute_count_accident")

    def compute_count_accident(self):
        for record in self:
            record.accident_count = self.env['accident.tracking'].search_count(
                [('employee_id', '=', self.id)]
            )
    def get_accident(self):
        return{
            'type': 'ir.actions.act_window',
            'name': 'Accidents',
            'view_mode': 'tree,form',
            'res_model': 'accident.tracking',
            'domain': [('employee_id', '=', self.id)],
            'context': "{'search_default_employee_id': [active_id], 'default_employee_id': active_id}",
        }