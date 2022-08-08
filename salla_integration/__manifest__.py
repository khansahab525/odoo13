# -*- coding: utf-8 -*-
{
    'name': "salla_integration",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'sale', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/stores.xml',
        'views/templates.xml',
        'views/configuration.xml',
        'views/res_partner_data.xml',
        'views/salla_integration.xml',
        'wizard/wizard_message.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
