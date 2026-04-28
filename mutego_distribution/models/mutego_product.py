# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MutegoProduct(models.Model):
    _name = 'mutego.product'
    _description = 'Mutego Distribution Product'
    _order = 'brand, name'
    _rec_name = 'name'

    name = fields.Char(
        string='Product Name',
        required=True,
        translate=True,
    )
    description = fields.Html(
        string='Description',
        translate=True,
    )
    brand = fields.Selection(
        selection=[
            ('pepsi', 'Pepsi'),
            ('7up', '7UP'),
            ('mountain_dew', 'Mountain Dew'),
            ('mirinda', 'Mirinda'),
            ('aquafina', 'Aquafina'),
            ('lipton', 'Lipton'),
            ('other', 'Other'),
        ],
        string='Brand',
        required=True,
        default='pepsi',
    )
    category = fields.Selection(
        selection=[
            ('carbonated', 'Carbonated Soft Drink'),
            ('water', 'Water'),
            ('juice', 'Juice & Nectars'),
            ('tea', 'Ready-to-Drink Tea'),
            ('energy', 'Energy Drink'),
            ('other', 'Other'),
        ],
        string='Category',
        required=True,
        default='carbonated',
    )
    volume_ml = fields.Integer(
        string='Volume (ml)',
    )
    image = fields.Image(
        string='Product Image',
        max_width=1024,
        max_height=1024,
    )
    image_thumb = fields.Image(
        string='Thumbnail',
        related='image',
        max_width=256,
        max_height=256,
        store=True,
    )
    is_active = fields.Boolean(
        string='Active',
        default=True,
    )
    is_featured = fields.Boolean(
        string='Featured on Homepage',
        default=False,
    )
    website_published = fields.Boolean(
        string='Published on Website',
        default=True,
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    slug = fields.Char(
        string='URL Slug',
        compute='_compute_slug',
        store=True,
    )

    @api.depends('name', 'brand', 'volume_ml')
    def _compute_slug(self):
        for record in self:
            base = f"{record.brand or 'product'}-{record.name or 'item'}"
            if record.volume_ml:
                base += f"-{record.volume_ml}ml"
            record.slug = base.lower().replace(' ', '-').replace('/', '-')

    def get_brand_label(self):
        self.ensure_one()
        return dict(self._fields['brand'].selection).get(self.brand, self.brand)

    def get_category_label(self):
        self.ensure_one()
        return dict(self._fields['category'].selection).get(self.category, self.category)
