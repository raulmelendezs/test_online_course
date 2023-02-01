# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class Course(models.Model): 
    
    _name = 'academy.course'
    _description = 'Course Info'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    
    level = fields.Selection(string='Level',
                             selection = [('beginner','Beginner'),
                                         ('intermediate','Intermediate'),
                                         ('advanced','Advanced')],
                             copy=False)
    active = fields.Boolean(string='Active', default=True)
    
    # Fields for Pricing
    base_price = fields.Float(string='Base Price', digits='Product Price', default=0.00)
    additional_fee = fields.Float(string='Additional Fee', digits='Product Price', default=10.00)
    total_price = fields.Float(string='Total Price', digits='Product Price', compute='_compute_total_price', readonly=True)
    
    sessions_id = fields.One2many(comodel_name='academy.session',
                                 inverse_name='course_id',
                                 string='Sessions')
    
    # --------------------------------------- Compute Methods ---------------------------------- 
    # Use Computed /depends field instead of OnChange in Odoo 16
    @api.depends('base_price', 'additional_fee')
    def _compute_total_price(self):
        for record in self:
            if record.base_price < 0.00:
                raise UserError(('Base Price cannot be set as Negative.'))
            
            record.total_price = record.base_price + record.additional_fee
    
    # --------------------------------------- Constrains Methods ----------------------------------
    @api.constrains('additional_fee')
    def _check_additional_fee(self):
        for record in self:
            if record.additional_fee < 10.00:
                raise ValidationError('Additional fees cannot be less than 10.00. Current Value %s' % record.additional_fee)