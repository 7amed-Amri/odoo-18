{
    'name': 'Vendor Registration',
    'version': '18.0.1.0.0',
    'category': 'Purchases/Website',
    'summary': 'Complete vendor registration system with website integration',
    'description': """
        Vendor Registration Module
        ==========================
        
        This module provides a complete vendor registration system with:
        * Website form for vendor registration
        * Backend management of vendor requests
        * Automatic partner creation upon approval
        * Multi-department support
        * Integration with Purchase Orders
        * Chatter for communication tracking
        * Bulk operations support
    """,
    'author': "KHELILI Hamza | TP Rihal",
    'website': "https://www.tpioneers.com/",    
    'license': 'OPL-1',
    'depends': ['purchase', 'website', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/website_menu.xml',
        'views/vendor_request_views.xml',
        'views/purchase_order_views.xml',
        'templates/website_templates.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}