# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import api, exceptions, fields, models
import openerp.addons.decimal_precision as dp
import datetime
import pdb

class product_category(models.Model):
    _inherit = "product.category"
    iscabintype = fields.Boolean('Is Cabin Type')

class cabin_type(models.Model):
    _name='cruise.cabin.type'
    _inherits = {'product.category':'cat_id'}
    cat_id = fields.Many2one('product.category', 'category', required=True, select=True, ondelete='cascade')

class cruise_cabin(models.Model):
    #_name = 'cruise.cabin'
    _description = 'Ship cabin'
    _inherit = "product.product"
    #_inherits = {'product.product' : 'product_id'}
    #product_id = fields.Many2one('product.product', 'Product', required=True, ondelete='restrict')
    ship_id = fields.Many2one('cruise.ship', 'Ship')
    cabin_type_id = fields.Many2one('cruise.cabin.type', 'Cruise cabin type'
       , help='Cruise cabin type')
    max_adult = fields.Integer('Max Adult')
    max_child = fields.Integer('Max Child')
    iscabin = fields.Boolean('Is Cabin', default=False)
    departure_ids = fields.Many2many('cruise.departure'
            , 'departure_cabin_rel'
            , 'departure_id'
            , 'cabin_id'
            , 'Departures'
            , help='Cabins in departure')
