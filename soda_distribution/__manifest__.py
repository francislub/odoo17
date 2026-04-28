# -*- coding: utf-8 -*-
{
    'name': 'Mutego Distribution Website',
    'version': '17.0.1.0.0',
    'category': 'Website',
    'summary': 'Corporate website for Mutego Distribution Company — authorized Pepsi & 7UP distributor',
    'description': """
        Mutego Distribution Company Website Module
        ==========================================
        This module provides a complete corporate website for Mutego Distribution Company,
        an authorized distributor of PepsiCo beverages (Pepsi, 7UP, Mountain Dew, Mirinda,
        Aquafina, Lipton) operating across multiple branches.

        Features:
        ---------
        * Home page with hero, stats, brands, and latest news
        * About Us page with company history, mission, and values
        * Products catalog with filtering by brand and category
        * Branches directory with location details
        * News & Announcements section
        * Contact Us form with branch selection
        * Backend management for all content
    """,
    'author': 'Mutego Distribution Company',
    'website': 'https://www.mutego.co.ke',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'website',
        'mail',
        'portal',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/mutego_product_views.xml',
        'views/mutego_branch_views.xml',
        'views/actions.xml',          
        'views/mutego_news_views.xml',
        'views/mutego_contact_views.xml',
        'views/website_templates.xml',
        'views/website_home.xml',
        'views/website_about.xml',
        'views/website_products.xml',
        'views/website_branches.xml',
        'views/website_news.xml',
        'views/website_contact.xml',
        'views/website_header_footer.xml',
        'views/website_menus.xml',
        'data/mutego_demo_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'mutego_distribution/static/src/css/mutego.css',
            'mutego_distribution/static/src/js/mutego.js',
        ],
    },
    'images': ['static/description/logo.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
}