{
    'name': 'hr employee',
    'version': '1.0',
    'summary': 'Employee personal sheet for Abigail Peterson',
    'description': 'Custom employee sheet for tracking personal and job info.',
    'author': 'Hamed ALanri',
    'category': 'Human Resources',
    'depends': ['base', 'hr'],
    'data': [
        'views/hr_employee_view.xml',
        'security /ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
