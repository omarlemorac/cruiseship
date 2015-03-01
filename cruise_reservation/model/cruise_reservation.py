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

    def _availability(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}
        res = {}
        departure_obj = self.browse(cr, uid, ids)


        for dep in departure_obj:
            dep_total_spaces = 0
            val = {}
            reqs = [req for req in dep.requisition_ids if req.state in
                    ('confirm','request', 'payment')]
            for req in reqs:
                dep_total_spaces += req.total_spaces
            val['availability_perc'] = ((float(dep.max_capacity) - float(dep_total_spaces)) / \
                    float(dep.max_capacity)) * 100
            val['availability'] = dep.max_capacity - dep_total_spaces
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
            'adult_unit_price':fields.float('Adult unit price'
                , help='Default adult unit price'),
            'child_unit_price':fields.float('Child unit price'
                , help='Child default adult unit price'),
            'young_unit_price':fields.float('Young unit price'
                , help='Young default adult unit price'),

            }


class reservation(osv.Model):

    '''
================================
Cruise reservation
================================
Reservation of cabins in cruise
-------------------------------
* Requisitions as lines of reservation
* A reservation is correspondent to a departure
    '''

    _name = 'class.name'

    _columns = {
            'name':fields.char('Name', 255, help='fields help'),
            }



class requisition(osv.Model):

    '''Requisition'''

    _name = 'cruise.rq'
    _rec_name = 'rq_no'

    def _availability(self, cr, uid, ids, field_name, arg, context=None):
        req_obj = self.browse(cr, uid, ids)
        res = {}

        for req in req_obj:
            fields = {}
            fields['availability'] = req['max_capacity'] - req['adults'] - req['young'] -\
               req['children']
            fields['availability_perc'] = (1 - ( float(fields['availability']) /
                    float(req['max_capacity']) )) * 100
            res[req.id] = fields
        return res

    def _total_spaces(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}

        res = {}
        req_obj = self.browse(cr, uid, ids)

        for req in req_obj:
            values = {}
            #res[req.id] = req['adults'] + req['young'] + req['children']
            adults = 0
            young = 0
            children = 0
            for rline in req.cruise_reservation_line_ids:
                adults += rline.adults
                young += rline.young
                children += rline.children
            values['adults'] = adults
            values['young'] = young
            values['children'] = children
            values['total_spaces'] = adults + young + children
            res[req.id] = values
        return res

    def _total_price(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}
        res = {}
        req_obj = self.browse(cr, uid, ids)

        for req in req_obj:
            fields = {}
            fields['adult_price_total'] = req['adults'] * req['adult_price_unit']
            fields['children_price_total'] = req['children'] * req['child_price_unit']
            fields['young_price_total'] = req['young'] * req['young_price_unit']
            fields['amount_total'] = fields['adult_price_total'] +\
                fields['children_price_total'] +\
                fields['young_price_total']
            res[req.id] = fields
        return res



    _columns = {
        'rq_no': fields.char('Reservation No'
            , size=64, required=True
            , readonly=True, states={'draft':[('readonly', False)]}),
        'reference':fields.char('Reference', 255, help='Passenger reference'),
        'order_contact_id':fields.many2one('res.partner'
            , string='Ordering contact', help='Ordering contact'
            , required=True, readonly=True, states={'draft':[('readonly', False)]}),
        'lead_id':fields.many2one('crm.lead', 'Lead'
           , help='Choose the lead for this requisition.'),
        'departure_id':fields.many2one('cruise.departure', 'Departure'
            , help='Departure', required=True, readonly=True
            , states={'draft':[('readonly', False)]}),
        'departure_ship_id':fields.related('departure_id', 'ship_id'
            , readonly=True,type="many2one", relation="cruise.ship"
            , help='Helper field ship'),

        'max_capacity':fields.related('departure_id', 'max_capacity'
            ,readonly=True, string='Maximum capacity', help='Maximum capacity'
            ,type="integer"),
        'availability':fields.related('departure_id', 'availability'
            ,readonly=True, string='Availability', type="integer"
            , help='Availability on departure'),
        'availability_perc':fields.related('departure_id', 'availability_perc'
            ,readonly=True, string='Availability percentage in departure'
            , help='Availability on departure'),
        'adults':fields.function(_total_spaces, method=True, store=False
            , fnct_inv=None, fnct_search=None, string='Adults'
            , help='Number of adults', multi="total_spaces"
            , type="integer"),
        'children':fields.function(_total_spaces, method=True, store=False
            , fnct_inv=None, fnct_search=None, string='Children'
            , help='Number of children', multi="total_spaces"
            , type="integer"),
        'young':fields.function(_total_spaces, method=True, store=False
            , fnct_inv=None, fnct_search=None, string='Young'
            , help='Number of young', multi="total_spaces"
            , type="integer"),
        'adult_price_unit':fields.float('Adult price', required=True
            ,digits_compute=dp.get_precision('Product Price')
            ,help='fields help'),
        'young_price_unit':fields.float('Young price', required=True
            ,digits_compute=dp.get_precision('Product Price')
            ,help='fields help'),
        'child_price_unit':fields.float('Child price', required=True
            ,digits_compute=dp.get_precision('Product Price')
            ,help='fields help'),
        'date_order':fields.date('Date order',required=True, help='Date order',
            readonly=True),
        'date_limit':fields.date('Date limit',required=True, help='Date limit'),
        'cruise_reservation_line_ids':fields.one2many('cruise.reservation.line'
            , 'rq_id', 'Reservation lines'
            , help='Reservation lines', readonly=True
            , states={'draft':[('readonly', False)]}),
        'account_voucher_ids':fields.one2many('account.voucher'
                , 'cruise_reservation_id', 'Payments'
                , help='Payments for this reservation'),


        'state': fields.selection([
               ('draft','Draft')
              ,('wlist','Waiting list')
              ,('request','Request')
              ,('confirm','Confirm')
              ,('payment','Payment')
              ,('paid','Paid')
              ,('cancel','Cancel')
              ,('done','Done')
              ]
            , 'State',readonly=True),

        'total_spaces':fields.function(_total_spaces, method=True, store=False
            , fnct_inv=None, fnct_search= None, string='Total spaces'
            , help='Total spaces reserved', multi="total_spaces"
            ),

        'adult_price_total':fields.function(_total_price, method=True, store=False
            , fnct_inv=None, fnct_search= None, string='Total adult', type="float"
            , help='Total price adult', multi='calc_totals'
            ),
        'children_price_total':fields.function(_total_price, method=True, store=False
            , fnct_inv=None, fnct_search= None, string='Total children', type="float"
            , help='Total price children', multi='calc_totals'
            ),
        'young_price_total':fields.function(_total_price, method=True, store=False
            , fnct_inv=None, fnct_search= None, string='Total young', type="float"
            , help='Total price children', multi='calc_totals'
            ),
        'amount_total':fields.function(_total_price, method=True, store=False
            , fnct_inv=None, fnct_search= None, string='Amount total', type="float"
            , help='Amount total', multi='calc_totals'
            ),
        }

    _defaults = {
        'adults':0,
        'children':0,
        'young':0,
        'rq_no': lambda obj, cr, uid, context:\
            obj.pool.get('ir.sequence').get(cr, uid,'cruise.requisition'),
        'state': lambda *a: 'draft',
        'date_order': fields.date.context_today,
        'date_limit': fields.date.context_today,
            }

    def onchange_departure(self, cr, uid, ids, departure_id, context=None):
        if context is None:
            context = {}

        res = {}
        if departure_id:
            departure_obj = self.pool.get('cruise.departure').browse(cr, uid,
                    departure_id)
            res['adult_price_unit'] = departure_obj.adult_price_normal
            res['child_price_unit'] = departure_obj.child_price_normal
            res['young_price_unit'] = departure_obj.young_price_normal
        return {'value':res}


    def cabin_sharing(pass1, pass2, cabins):
        if context is None:
            context = {}

        return

    def _read_capacity(self, cr, uid, ids,context=None):
        """Return capacity of cabins _in departure"""
        if context is None:
            context = {}
        res = {}
        for req in self.browse(cr, uid, ids, context=context):
            for cabin in req.departure_id.ship_id.cabin_ids:
                res[cabin.id] = (cabin.max_adult, cabin.max_child)
        return res
    def _cabin_dict(self, cr, uid, ids,context=None):
        """Return capacity of cabins _in departure"""
        if context is None:
            context = {}
        res = {}
        for req in self.browse(cr, uid, ids, context=context):
            for cabin in req.departure_id.ship_id.cabin_ids:
                res[cabin.id] = []
        return res

    def _read_reservations(self, cr, uid, ids, context=None):
        """docstring for _read_reservations"""
        if context is None:
            context = {}
        reservations = []
        res = []
        r = []
        for req in self.browse(cr, uid, ids, context=context):
            req_d = []
            req_d.append(req.rq_no)
            reservation_ids = self.search(cr, uid
                    , [('state', 'in', ('request', 'confirm', 'payment', 'paid',
                        'done')),
                       ('departure_id.id', '=',req.departure_id.id), #la misma salida
                       ('id', '!=', ids[0]),
                        ], context=context)

            for rs in self.browse(cr, uid, reservation_ids):
                line = []
                for rs_line in rs.cruise_reservation_line_ids:
                    line.append((rs.rq_no, rs_line.id, rs_line.sharing,
                        rs_line.adults + rs_line.young))
                    cabins = []
                    for cabin in rs_line.cabin_ids:
                        cabins.append(cabin.id)
                    line.append(cabins)
                req_d.append(line)
            reservations.append(r)
            res.append(req_d)
        return res

    def _check_self_reservation(self, cr, uid, active_id):
        """Compare availability _with reserved_cabins."""

        res_obj = self.browse(cr, uid, active_id)
        print res_obj.rq_no
        return False

    def _search_departure_cabins(self, cr, uid, ids, context=None):
        """
        male sharing only allows adults
        female sharing only allows adults

                                if cabin in [r[1] for r in reserved_cabins['no_sharing']]:
                                    msg = "%s are already reserved cabins without sharing"\
                                          % ", ".join(["%s %s" % (n[0].rq_no, n[1].name) for n in
                                                reserved_cabins['no_sharing']])
        """
        if context is None:
            context = {}

        msg = ""

        capacity = self._read_capacity(cr, uid, ids)
        print "\n====================capacity==================="
        print capacity
        print self._cabin_dict(cr,uid, ids)
        reserved_cabins = self._read_reservations(cr, uid, ids)

        print reserved_cabins
        print "stop"

        """basic validation. Maximum capacity"""
        '''
        for line in req.cruise_reservation_line_ids:
            av_adults = 0
            av_children = 0
            if line.adults + line.young > capacity[cabin.id][0]:
                raise osv.except_osv('Warning'
                , 'Maximum adult capacity reached')
            if line.children > capacity[cabin.id][1]:
                raise osv.except_osv('Warning'
                , 'Maximum children capacity reached')
        '''

        return False

    def action_request(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        self_reservation = self._check_self_reservation(cr, uid, context['active'] )
        print self_reservation

        for req in self.browse(cr, uid, ids, context=context):
            if req.total_spaces < 1:
                raise osv.except_osv('Warning', 'You must have at least one passenger')

            for line in req.cruise_reservation_line_ids:
                if not line.cabin_ids:
                    raise osv.except_osv('Warning', 'Cabins must be setted')

        return self._search_departure_cabins(cr, uid, ids)\
                and self.write(cr, uid, ids, {'state':'draft'})\
                or self.write(cr, uid, ids, {'state':'wlist'})

        #return self.write(cr, uid, ids, {'state':'request'})

    def action_cancel(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        raise osv.except_osv('Warning',' you cant cancel. :(')
        return self.write(cr, uid, ids, {'state':'cancel'})

class reservation_line(osv.Model):

    '''Reservation detail for cabin'''

    _name = 'cruise.reservation.line'

    _columns = {
        'name':fields.char('Name', 255, help='ReferenceX', required=False,
            placeholder="e.g. ReferenceX#"),
        'rq_id':fields.many2one('cruise.rq', 'Requisition Id'
            , help='Id for requisition'),
        'line_departure_ship_id':fields.related('rq_id'
            , 'departure_ship_id', readonly=True
            , relation="cruise.ship", string='Ship', type="many2one"
            , help='Helper field to filter cabins'),

        'line_departure_id':fields.related('rq_id'
            , 'departure_id', readonly=True
            , relation="cruise.departure", string='Departure', type="many2one"
            , help='Helper field to filter cabins'),

        'adults':fields.integer('Adult', help='Number of adults'
            ,required=True),
        'children':fields.integer('Children',required=True, help='Number of children'),
        'young':fields.integer('Young',required=True, help='Number of young'),
        'cabin_ids':fields.many2many('cruise.cabin', 'reservation_cabin_rel',
            'rq_line_id', 'cabin_id', 'Cabins', help='Cabins reserved',
            domain="[('ship_id', '=', line_departure_ship_id)]"),
        'sharing':fields.selection([
            ('male_sharing', 'Male sharing'),
            ('female_sharing', 'Female sharing'),
            ('no_sharing', 'No sharing'),
            ], string='Sharing type', required=True,
            help='Select the sharing type for cabin/s'),

        }

class cruise_cabin(osv.Model):

    '''Inherits cruise.cabin to add m2m relationship with reservation line'''

    _inherit = 'cruise.cabin'

    _columns = {
        'res_ids':fields.many2many('cruise.reservation.line', 'reservation_cabin_rel',
            'cabin_id','rq_line_id','Reservations',
            help='Reservations made to cabin'),

        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
