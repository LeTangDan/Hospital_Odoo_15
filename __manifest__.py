# -*- coding:utf-8 -*-
{
    'name': 'Hospital Management',
    'version': '14.0.1',
    'sequence': 2,
    'author': 'Daihv dev',
    'category': 'Services/Project',
    'summary': 'Quản lý phòng khám tư nhân',
    'description': """
    """,
    'website': 'https://www.facebook.com/Daihv96',
    'depends': ['base', 'mail'],
    'data': [
        # 'security/hospital_security.xml',
        'security/ir.model.access.csv',

        'report/menu_report.xml',

        'views/doctor_info_view.xml',
        'views/examine_history_info_view.xml',
        'views/payment_history_view.xml',
        'views/medicine_info_view.xml',
        'views/sick_persion_info_view.xml',
        'views/schedule_examine_view.xml',
        'views/message_server_config_view.xml',
        'views/master_data_view.xml',
        'views/hospital_info_view.xml',
        'views/special_customer_view.xml',
        'views/potential_patient_view.xml',
        'report/templates.xml',
        'data/cron_job_auto_sent_msg.xml',
        'wizards/send_msg_wizard.xml',
        'wizards/confirm_msg_unlink.xml',
        'wizards/sick_persion_info_search_view.xml',

        'menuitem.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}


