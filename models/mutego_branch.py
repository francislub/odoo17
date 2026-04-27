# -*- coding: utf-8 -*-
from odoo import models, fields


class MutegoBranch(models.Model):
    _name = 'mutego.branch'
    _description = 'Mutego Distribution Branch'
    _order = 'is_headquarters desc, name'
    _rec_name = 'name'

    name = fields.Char(
        string='Branch Name',
        required=True,
        translate=True,
    )
    address = fields.Text(
        string='Street Address',
        required=True,
    )
    city = fields.Char(
        string='City',
        required=True,
    )
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country',
        required=True,
    )
    phone = fields.Char(
        string='Phone Number',
    )
    email = fields.Char(
        string='Email Address',
    )
    manager_name = fields.Char(
        string='Branch Manager',
    )
    is_headquarters = fields.Boolean(
        string='Is Headquarters',
        default=False,
    )
    latitude = fields.Float(
        string='Latitude',
        digits=(10, 7),
    )
    longitude = fields.Float(
        string='Longitude',
        digits=(10, 7),
    )
    image = fields.Image(
        string='Branch Image',
        max_width=1024,
        max_height=1024,
    )
    description = fields.Html(
        string='Description',
        translate=True,
    )
    working_hours = fields.Char(
        string='Working Hours',
        default='Mon - Fri: 8:00 AM - 5:00 PM',
    )
    website_published = fields.Boolean(
        string='Published on Website',
        default=True,
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
