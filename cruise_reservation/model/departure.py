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
import operator as O
import pdb



class departure(osv.Model):

    '''Requisition and Reservation on departure'''

    _name = 'cruise.departure'
    _inherit = 'cruise.departure'

    def _spaces_calc(self, reservation_obj):
        """Calculate spaces with sharing option"""
        total_res = 0
        for line in reservation_obj.cruise_reservation_line_ids:
            if line.sharing == 'no_sharing':
                total_res += line.cabin_id.max_adult
            else:
                total_res += line.adults + line.young
        return total_res


    def _requested_count(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}
        return self._count_reserved(cr,uid,ids,'request')

    def _confirmed_count(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}
        return self._count_reserved(cr,uid,ids,'confirm')

    def _count_reserved(self, cr, uid, ids, state):
        res = {}
        departure_obj = self.browse(cr, uid, ids)

        for dep in departure_obj:
            total_spaces = 0
            for r in [req for req in dep.requisition_ids if req.state ==
                    state]:
                total_spaces += self._spaces_calc(r)
            res[dep.id] =  total_spaces
        return res

    def _availability(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}
        res = {}
        departure_obj = self.browse(cr, uid, ids)

        for dep in departure_obj:
            dep_total_spaces = 0
            val = {}
            availability_total = 0
            for c in dep.ship_id.cabin_ids:
                availability_total += c.max_adult

            reqs = [req for req in dep.requisition_ids if req.state in
                    ('confirm','request')]
            for req in reqs:
                dep_total_spaces += self._spaces_calc(req)
            val['availability_perc'] = ((float(dep.max_capacity) - float(dep_total_spaces)) / \
                    float(dep.max_capacity)) * 100
#            val['availability'] = dep.max_capacity - dep_total_spaces
            val['availability'] = availability_total - dep_total_spaces
            res[dep.id] = val
        return res

    def _search_availability(self, cr, uid, ids, field_name, args, context=None):
        if context is None:
            context = {}
        obj = self.search(cr, uid, [])
        ava = self._availability(cr, uid, obj, field_name, args)
        r_ids = []
        for a, avd in ava.items():
            av = avd['availability']
            for arg in args:
                if arg[0] == 'availability':
                    if arg[1] == '=':
                        if int(av) == int(arg[2]):
                            r_ids.append(a)
                    if arg[1] == '<':
                        if int(av) < int(arg[2]):
                            r_ids.append(a)
                    if arg[1] == '>':
                        if int(av) > int(arg[2]):
                            r_ids.append(a)
        return [('id', 'in', r_ids)]

    _columns = {
            'requisition_ids':fields.one2many('cruise.rq'
                , 'departure_id', 'Requisitions', help='Requisitions'),
            'adult_unit_price':fields.float('Adult unit price'
                , help='Default adult unit price'),
            'child_unit_price':fields.float('Child unit price'
                , help='Child default adult unit price'),
            'young_unit_price':fields.float('Young unit price'
                , help='Young default adult unit price'),
            'availability':fields.function(_availability
                , method=True, store=False, fnct_inv=None
                , fnct_search=_search_availability, string='Availability'
                , help='Availability', type='integer'
                , multi='check_availability'),
            'availability_perc':fields.function(_availability
                , method=True, store=False, fnct_inv=None
                , fnct_search=None, string='Availability'
                , help='Availability', type='float'
                , multi='check_availability'),
            'requested_count':fields.function(_requested_count
                , method=True, store=False, fnct_inv=None
                , fnct_search=None, string='Requested'
                , help='Adult count on requested reservations', type='integer'
                ),
            'confirmed_count':fields.function(_confirmed_count
                , method=True, store=False, fnct_inv=None
                , fnct_search=None, string='Confirmed'
                , help='Adult count on confirmed reservations', type='integer'
                ),

            }
