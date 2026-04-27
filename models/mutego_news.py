# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import html_translate


class MutegoNews(models.Model):
    _name = 'mutego.news'
    _description = 'Mutego Distribution News & Announcements'
    _order = 'published_date desc'
    _rec_name = 'title'

    title = fields.Char(
        string='Title',
        required=True,
        translate=True,
    )
    summary = fields.Text(
        string='Summary',
        required=True,
        translate=True,
    )
    content = fields.Html(
        string='Full Content',
        translate=html_translate,
    )
    image = fields.Image(
        string='Featured Image',
        max_width=1200,
        max_height=800,
    )
    image_thumb = fields.Image(
        string='Thumbnail',
        related='image',
        max_width=400,
        max_height=300,
        store=True,
    )
    published_date = fields.Date(
        string='Published Date',
        required=True,
        default=fields.Date.today,
    )
    author = fields.Char(
        string='Author',
        default='Mutego Distribution',
    )
    is_featured = fields.Boolean(
        string='Featured on Homepage',
        default=False,
    )
    website_published = fields.Boolean(
        string='Published on Website',
        default=False,
    )
    tag_ids = fields.Many2many(
        comodel_name='mutego.news.tag',
        string='Tags',
    )
    slug = fields.Char(
        string='URL Slug',
        compute='_compute_slug',
        store=True,
    )

    @api.depends('title', 'published_date')
    def _compute_slug(self):
        for record in self:
            title_slug = (record.title or 'news').lower().replace(' ', '-')
            title_slug = ''.join(c if c.isalnum() or c == '-' else '' for c in title_slug)
            record.slug = f"{title_slug}-{record.id or 0}"


class MutegoNewsTag(models.Model):
    _name = 'mutego.news.tag'
    _description = 'News Tag'
    _rec_name = 'name'

    name = fields.Char(string='Tag', required=True, translate=True)
    color = fields.Integer(string='Color Index')
