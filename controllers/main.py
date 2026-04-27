# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class MutegoWebsite(http.Controller):

    # -------------------------------------------------------------------------
    # Home Page
    # -------------------------------------------------------------------------
    @http.route('/', type='http', auth='public', website=True, sitemap=True)
    def home(self, **kwargs):
        featured_products = request.env['mutego.product'].sudo().search([
            ('website_published', '=', True),
            ('is_featured', '=', True),
        ], limit=6)
        all_products = request.env['mutego.product'].sudo().search([
            ('website_published', '=', True),
        ], limit=12)
        branches = request.env['mutego.branch'].sudo().search([
            ('website_published', '=', True),
        ])
        latest_news = request.env['mutego.news'].sudo().search([
            ('website_published', '=', True),
        ], limit=3)

        brands = list({p.brand for p in all_products if p.brand})

        values = {
            'featured_products': featured_products,
            'branches': branches,
            'latest_news': latest_news,
            'brands': brands,
            'total_products': request.env['mutego.product'].sudo().search_count([
                ('website_published', '=', True),
            ]),
            'total_branches': request.env['mutego.branch'].sudo().search_count([
                ('website_published', '=', True),
            ]),
        }
        return request.render('mutego_distribution.homepage', values)

    # -------------------------------------------------------------------------
    # About Us
    # -------------------------------------------------------------------------
    @http.route('/about', type='http', auth='public', website=True, sitemap=True)
    def about(self, **kwargs):
        return request.render('mutego_distribution.about_page', {})

    # -------------------------------------------------------------------------
    # Products
    # -------------------------------------------------------------------------
    @http.route('/products', type='http', auth='public', website=True, sitemap=True)
    def products(self, brand=None, category=None, **kwargs):
        domain = [('website_published', '=', True)]
        if brand:
            domain.append(('brand', '=', brand))
        if category:
            domain.append(('category', '=', category))

        products = request.env['mutego.product'].sudo().search(domain, order='brand, name')

        brand_options = request.env['mutego.product'].sudo().fields_get(['brand'])['brand']['selection']
        category_options = request.env['mutego.product'].sudo().fields_get(['category'])['category']['selection']

        values = {
            'products': products,
            'brand_options': brand_options,
            'category_options': category_options,
            'current_brand': brand,
            'current_category': category,
        }
        return request.render('mutego_distribution.products_page', values)

    @http.route('/products/<int:product_id>', type='http', auth='public', website=True, sitemap=True)
    def product_detail(self, product_id, **kwargs):
        product = request.env['mutego.product'].sudo().browse(product_id)
        if not product.exists() or not product.website_published:
            return request.not_found()

        related = request.env['mutego.product'].sudo().search([
            ('brand', '=', product.brand),
            ('website_published', '=', True),
            ('id', '!=', product.id),
        ], limit=4)

        values = {
            'product': product,
            'related_products': related,
        }
        return request.render('mutego_distribution.product_detail_page', values)

    # -------------------------------------------------------------------------
    # Branches
    # -------------------------------------------------------------------------
    @http.route('/branches', type='http', auth='public', website=True, sitemap=True)
    def branches(self, **kwargs):
        branches = request.env['mutego.branch'].sudo().search([
            ('website_published', '=', True),
        ], order='is_headquarters desc, name')

        values = {
            'branches': branches,
        }
        return request.render('mutego_distribution.branches_page', values)

    # -------------------------------------------------------------------------
    # News
    # -------------------------------------------------------------------------
    @http.route('/news', type='http', auth='public', website=True, sitemap=True)
    def news(self, **kwargs):
        news_items = request.env['mutego.news'].sudo().search([
            ('website_published', '=', True),
        ], order='published_date desc')

        values = {
            'news_items': news_items,
        }
        return request.render('mutego_distribution.news_page', values)

    @http.route('/news/<int:news_id>', type='http', auth='public', website=True, sitemap=True)
    def news_detail(self, news_id, **kwargs):
        news = request.env['mutego.news'].sudo().browse(news_id)
        if not news.exists() or not news.website_published:
            return request.not_found()

        other_news = request.env['mutego.news'].sudo().search([
            ('website_published', '=', True),
            ('id', '!=', news.id),
        ], limit=3, order='published_date desc')

        values = {
            'news': news,
            'other_news': other_news,
        }
        return request.render('mutego_distribution.news_detail_page', values)

    # -------------------------------------------------------------------------
    # Contact Us
    # -------------------------------------------------------------------------
    @http.route('/contact', type='http', auth='public', website=True, sitemap=True)
    def contact(self, **kwargs):
        branches = request.env['mutego.branch'].sudo().search([
            ('website_published', '=', True),
        ])
        values = {
            'branches': branches,
            'success': kwargs.get('success', False),
        }
        return request.render('mutego_distribution.contact_page', values)

    @http.route('/contact/submit', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def contact_submit(self, **post):
        required = ['name', 'email', 'message']
        for field in required:
            if not post.get(field, '').strip():
                branches = request.env['mutego.branch'].sudo().search([
                    ('website_published', '=', True),
                ])
                return request.render('mutego_distribution.contact_page', {
                    'branches': branches,
                    'error': f'Please fill in the required field: {field}.',
                    'form_data': post,
                })

        vals = {
            'name': post.get('name', '').strip(),
            'email': post.get('email', '').strip(),
            'phone': post.get('phone', '').strip(),
            'subject': post.get('subject', '').strip(),
            'message': post.get('message', '').strip(),
        }
        branch_id = post.get('branch_id')
        if branch_id:
            try:
                vals['branch_id'] = int(branch_id)
            except (ValueError, TypeError):
                pass

        request.env['mutego.contact'].sudo().create(vals)

        return request.redirect('/contact?success=1')
