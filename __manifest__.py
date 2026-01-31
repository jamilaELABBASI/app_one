{
    'name': "App One",
    'author': "Jamila ELABBASI",
    'category': "Real Estate",
    'version': "19.0.0.1.0",

    # modules nécessaires
    'depends': ['base','sale_management','sale','account','contacts'],

    # fichiers de données
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/property_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
        'views/building_view.xml',
        'reports/property_report.xml',
        'data/sequence.xml',
        'views/property_history_view.xml',
        'views/change_state_wizard_view.xml',
        'views/product_template_view.xml',
    ],
    # styles CSS
    'assets':{
        'web.assets_backend':['app_one/static/src/css/property.css',
                              'app_one/static/src/js/listView.js',
                              'app_one/static/src/xml/listView.xml'
                              ],

        'web_report_assets_common':[
            'app_one/static/src/css/font.css',

                                    ]
    },
    # important !
    'application': True,
    "license": "LGPL-3",

}
