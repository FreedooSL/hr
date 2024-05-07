# -*- coding: utf-8 -*-
# © 2023 Soluciones Tecnológicas Freedoo: Stephany Zegarra Tejada <stephany@freedoo.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _
import base64

class AccidentTrackingReportWiz(models.TransientModel):
    _name = 'accident.tracking.report.wiz'
    _decription = 'Wizard to print accident report'

    accident_id = fields.Many2one(comodel_name="accident.tracking")
    type_accident = fields.Selection(string="The accident is ...",
                                     selection=[('with', 'Accident with sick leave'),
                                                ('without', 'Accident without sick leave')])
    report_id = fields.Many2one(comodel_name="ir.actions.report",
                                     string="Report")

    def action_get_attachment(self):
        if self.type_accident == 'with':
            name = "sistema-delta-unigemsa"
            
            pdf_file = self.env['ir.actions.report']._render_qweb_pdf('hr_accident_mutual_insurance.action_accident_unigemsa_report', self.id)
            pdf_file = pdf_file[0]
            self.pdf_file = base64.b64encode(pdf_file)

        elif self.type_accident == 'without':
            name = "volante-fremap"

            pdf_file = self.env['ir.actions.report']._render_qweb_pdf('hr_accident_mutual_insurance.action_accident_fremap_report', self.id)
            pdf_file = pdf_file[0]
            self.pdf_file = base64.b64encode(pdf_file)

        return self.env['ir.attachment'].create({
            'name': name,
            'type': 'binary',
            #'datas_fname': name + '.pdf',
            'store_fname': name,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/x-pdf'
        })

    def print_report_accident(self):
        new_att = self.env.ref('hr_accident_mutual_insurance.action_for_accident_incident_investigation_report').report_action(self)
        return new_att

    def done(self):
        save_attach = self.action_get_attachment()
        if self.type_accident == 'with':
            name = 'Sistema Delta (Unigemsa)'
        elif self.type_accident == 'without':
            name = 'Volante Fremap'
        self.accident_id.tracking_report_ids = [(0, 0, {'name': name,
                                                        'attachment_id': save_attach.id,})]
        xml_id = self.report_id.xml_id
        new_att = self.env.ref(xml_id).report_action(self)
        return new_att