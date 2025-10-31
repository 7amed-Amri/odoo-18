{
    'name': 'Correspondence',
    'version': '1.0',
    'category': 'Administration',
    'summary': 'Manage Correspondence Records',
    'description': 'Module to manage incoming and outgoing correspondence.',
    'author': 'Hamed',
    'website': 'https://Hamed.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/correspondence_views.xml',
    ],
    'installable': True,
    'application': True,
    'images': ['static/description/icon.png'],  # Add this line
}