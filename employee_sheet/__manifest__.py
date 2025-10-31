{
    'name': 'Employee Sheet',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Custom Employee Sheet Fields',
    'depends': ['hr'],
    'data': [
        'security/employee_sheet_security.xml',
        'views/employee_sheet_view.xml',
    ],

    'installable': True,
    'application': False,
}
