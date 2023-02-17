# Copyright (c) 2020-Present Autodidacta TI. (<https://autodidactati.com>)

{
    'name': 'Reporte de Ventas diarias en POS',
    "version": "11.0",
    'author': 'Ivan Arriola - Autodidacta TI',
    'category': 'Extra Tools',
    'license': 'OPL-1',
    'website': 'https://autodidactati.com',
    'summary': 'Reporte de Ventas diarias en POS',
    'description': '''Este reporte muestra caracteristicas de ventas del punto de venta''',
    'depends': ['point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/report_wizard_view.xml',
        'report/daily_sales_pos_report.xml',
    ],
    'installable': True,
    'auto_install': False
}
