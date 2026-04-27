# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class MutegoContact(models.Model):
    _name = 'mutego.contact'
    _description = 'Mutego Website Contact Form Submission'
    _order = 'create_date desc'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Full Name',
        required=True,
        tracking=True,
    )
    email = fields.Char(
        string='Email Address',
        required=True,
        tracking=True,
    )
    phone = fields.Char(
        string='Phone Number',
    )
    subject = fields.Char(
        string='Subject',
    )
    message = fields.Text(
        string='Message',
        required=True,
    )
    branch_id = fields.Many2one(
        comodel_name='mutego.branch',
        string='Related Branch',
    )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('in_progress', 'In Progress'),
            ('resolved', 'Resolved'),
            ('closed', 'Closed'),
        ],
        string='Status',
        default='new',
        tracking=True,
    )
    notes = fields.Text(
        string='Internal Notes',
    )

    @api.constrains('email')
    def _validate_email(self):
        for record in self:
            if record.email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', record.email):
                raise ValidationError('Please enter a valid email address.')
