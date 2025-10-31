{
    'name': 'Support Ticket System',
    'version': '18.0.1.0.0',
    'category': 'Services/Helpdesk',
    'summary': 'Website help desk ticket system with approval workflow',
    'description': """
Support Ticket System
====================
* Website form for ticket submission
* Backend approval workflow
* Ticket management system
* Email notifications (optional)
""",
    'author': "Your Name",
    'website': "https://yourwebsite.com",
    'depends': ['website', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/support_ticket_views.xml',
        'views/website_templates.xml',
        'views/website_menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
