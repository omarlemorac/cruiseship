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
from openerp import tools
import openerp.addons.decimal_precision as dp
import operator as O
import pdb

class cruise_departure_availability(osv.Model):

    '''Cruise departure availability report'''

    _name = 'cruise.departureavailabilityvw'
    _description = 'Cruise departure availability report'
    _auto = False

    _columns = {'departure':fields.char('Departure', 255, help='Departure'),
                'ship':fields.char('Ship', 255, help='Ship'),
                'departure_date':fields.date('Departure Date'),
                'arrival_date':fields.date('Arrival Date'),
                'itinerary':fields.char('Ititnerary',
                    help='Ititnerary'),
                'adult_price_normal':fields.float('Adult Price Normal'),
                'adult_price_unit':fields.float('Adult Price Unit'),
                'young_price_normal':fields.float('Young Price Normal'),
                'young_price_unit':fields.float('Young Price Unit'),
                'child_price_normal':fields.float('Child Price Normal'),
                'child_price_unit':fields.float('Child Price Unit'),
                'max_pax':fields.integer('Ship Capacity'),
                'cabin':fields.char('Cabin', 255, help='Cabin'),
                'adults':fields.integer('Adults'),
                'young':fields.integer('Young'),
                'children':fields.integer('Children'),
                'sharing':fields.char('Sharing', 255, help='Sharing'),
                'reservation':fields.char('Reservation', 255, help='Reservation'),
                'ordering_partner':fields.char('Ordering Partner', 255,
                    help='Ordering Partner'),
                'salesperson':fields.char('Sales Person', 255
                    , help='Sales Person'),
                'state':fields.char('State', 255, help='State'),
                'date_request':fields.date('Date Request', help='Date Request'),
                'date_limit':fields.date('Date Limit', help='Date Limit'),
                'departure_id':fields.integer('Departure Id'),
                'ship_id':fields.integer('Ship Id'),

    }

    def init(self, cr):
            tools.sql.drop_view_if_exists(cr, 'cruise.departureavailabilityvw')
            cr.execute(
                """
                CREATE OR REPLACE VIEW cruise_departureavailabilityvw AS
                select cast(cast(d.id as text) || cast(c.id as text) || cast(coalesce(r.id, 0) as text)
                || cast(coalesce(l.id, 0) as text) as integer) id, d.name departure, s.name Ship, d.departure_date, d.arrival_date, d.itinerary, d.adult_price_normal,
                r.adult_price_unit, d.young_price_normal, r.young_price_unit, d.child_price_normal, r.child_price_unit,
                s.max_pax, cast(c.id as text) cid, c.name cabin, l.adults, l.children, l.young, l.sharing, r.reference reservation, p.name ordering_partner,
                up.name salesperson, r.state, date_request, date_limit, d.id
                departure_id, s.id ship_id
                from cruise_departure d
                inner join cruise_ship s
                  on d.ship_id = s.id
                inner join cruise_cabin c
                  on s.id = c.ship_id
                left join cruise_reservation_line l
                  on c.id = l.cabin_id
                left join (select * from cruise_rq where state not in ('draft', 'cancel')) r
                  on l.rq_id = r.id
                left join res_partner p
                  on r.order_contact_id = p.id
                left join res_users u
                  on r.user_id = u.id
                left join res_partner up
                  on u.partner_id = up.id
                order by d.name, c.name

                """
                )

