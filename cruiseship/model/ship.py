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

from osv import osv, fields
import openerp.addons.decimal_precision as dp


class cruise_ship(osv.Model):
    _name = "cruise.ship"
    _description = "Ship"
    _columns = {
        'name': fields.char('Ship Name', size=64, required=True, select=True),
        'sequence' : fields.integer('Sequence', size=64),
        'observations' : fields.html('Observations'),
        'max_pax':fields.integer('Maximum capacity'
            , help='Maximum passenger number allowed in law'),
        'cabin_ids':fields.one2many('cruise.cabin', 'ship_id', 'Cabins'
            , help='Add cabins to this ship'),
        'check_max_capacity':fields.boolean('Check maximum capacity'
            , help='Check maximum capacity in reserving'),
        }
    _defaults={
        'check_max_capacity':False,
            }

class product_product(osv.osv):
    _inherit = "product.product"
    _columns = {
        'isroom':fields.boolean('Is Room'),
        'iscategid':fields.boolean('Is categ id'),
        'isservice':fields.boolean('Is Service id'),
    }

class cabin_type(osv.Model):
    _name='cruise.cabin.type'
    _columns = {
        'name':fields.char('Name', 255, help='Name of cabin type'),
            }


class cruise_cabin(osv.Model):
    _name = 'cruise.cabin'
    _description = 'Ship cabin'
    _columns = {
        'name':fields.char('Name', 255, help='Name', required=True),
        'ship_id':fields.many2one('cruise.ship', 'Cabin'),
        'cabin_type_id':fields.many2one('cruise.cabin.type', 'Cruise cabin type'
            , help='Cruise cabin type'),
        'max_adult':fields.integer('Max Adult'),
        'max_child':fields.integer('Max Child'),
        }

class cabin_pax_line(osv.Model):

    '''Pax reserving cabin'''

    _name = 'cabin.pax.line'
    _columns = {
        'pax_id':fields.many2one('res.partner', 'Pax', help='Pax using cabin'),
        'age_ref':fields.selection([
            ('adult','Adult'),
            ('young','Young'),
            ('child','Child'),
            ]
            , string='Age reference'
            , help='Age reference'),
        'bed_space_adult':fields.integer('Bed Space Adult', help='Bed space adult'),
        'bed_space_child':fields.integer('Bed Space Child', help='Bed space child'),
        }

class departure_cabin_line(osv.Model):
    _name = 'departure.cabin.line'
    _description = 'Line for cabin in departure'
    _columns = {
        'cabin_id':fields.many2one('cruise.cabin', 'Cabin', help='Add a cabin for departure'),
        'departure_id':fields.many2one('cruise.departure', 'Departure'
            , help='Departure'),
        'ship_id':fields.related('cabin_id'
            , 'ship_id'
            , readonly=True
            , type='many2one'
            , relation='cruise.ship'
            , string='Ship'
            , help='Ship related to cabin '),
        }

class departure_ship_line(osv.Model):

    '''Ships on departure'''

    _name = 'departure.ship.line'

    _columns = {
        'ship_id':fields.many2one('cruise.ship', 'Ship', help='Add a ship for departure'),
        'departure_id':fields.many2one('cruise.departure', 'Departure'
            , help='Departure'),
        'max_capacity':fields.related('ship_id'
            , 'max_pax'
            , readonly=True
            , type='integer'
            , string='Maximum Capacity'
            , help='Maximum capacity of ship'),
        }


class departure(osv.Model):
    _name = 'cruise.departure'
    _description = 'Cruise Departure'
    _columns = {
        'name':fields.char('Name', 255, help='fields help'),
        'departure_date':fields.date('Departure date', help='Departure date'),
        'arrival_date':fields.date('Arrival date', help='Arrival date'),
        'observations':fields.html('Observations', help='Observations'),
        'ship_id':fields.many2one('cruise.ship', 'Ship', help='Add a ship for departure'),
        'itinerary':fields.char('Itinerary', 50, help='Itinerary for this departure '),
        'max_capacity':fields.related(
              'ship_id'
            , 'max_pax'
            , readonly=True
            , type='integer'
            , string='Maximum Capacity'
            , help='Maximum capacity of ship'),
        'adult_price_normal':fields.float('Adult price', required=True
            ,digits_compute=dp.get_precision('Product Price')
            ,help='fields help'),
        'young_price_normal':fields.float('Young price', required=True
            ,digits_compute=dp.get_precision('Product Price')
            ,help='fields help'),
        'child_price_normal':fields.float('Child price', required=True
            ,digits_compute=dp.get_precision('Product Price')
            ,help='fields help'),


            }
