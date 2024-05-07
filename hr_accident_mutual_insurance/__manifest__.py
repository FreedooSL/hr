# -*- coding: utf-8 -*-
# © 2023 Soluciones Tecnológicas Freedoo: Stephany Zegarra Tejada <stephany@freedoo.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Employee accident record',
    'category': '',
    'summary': 'Accident record',
    'version': '16.0.1.0.0',
    'author': 'Soluciones Tecnológicas Freedoo',
    'website': 'https://www.freedoo.es',
    'depends': [
        'hr_accident_report_tracking',
    ],
    'data': [
        'views/accident_tracking_inherit_view.xml',
        'wizards/accident_tracking_wizard.xml',
        'reports/hr_employee_accident_fremap_report.xml',
        'reports/hr_employee_accident_unigemsa_report.xml',
        'security/ir.model.access.csv',
    ],

    'demo': [
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}