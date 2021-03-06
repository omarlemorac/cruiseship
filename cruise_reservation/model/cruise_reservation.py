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
    _inherit = ['mail.thread', 'ir.needaction_mixin']

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
        'reference':fields.char('Reference', 255, help='Passenger reference', required=True),
        'order_contact_id':fields.many2one('res.partner'
            , string='Ordering contact', help='Ordering contact'
            , required=True, readonly=True, states={'draft':[('readonly', False)]}),
        'user_id': fields.many2one('res.users', 'Salesperson', select=True,required=True ),
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
        'date_limit':fields.date('Date limit',required=True, help='Date limit'),
        'date_request':fields.date('Date request',required=True, help='Date request'),
        'date_confirm':fields.date('Date confirm',required=True, help='Date confirm',
            readonly=False),
        'date_payment':fields.date('Date payment',required=True, help='Date payment'),
        'date_paid':fields.date('Date paid',required=True, help='Date paid'),
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
              ,('cancel','Cancel')
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
        'date_confirm': fields.date.context_today,
        'date_limit': fields.date.context_today,
        'date_request': fields.date.context_today,
        'date_payment': fields.date.context_today,
        'date_paid': fields.date.context_today,
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

    def _find_duplicated(self, values):
        """docstring for _find_duplicated_cabin"""
        values['cabins'].sort()
        cabin_l = [c['cabin_id'] for c in values['cabins']]
        duplicates = []
        for c in cabin_l:
            if cabin_l.count(c) > 1:
                duplicates.append(c)
        return set(duplicates)


    def _read_capacity(self, cr, uid, ids,context=None):
        """Return capacity of cabins _in departure"""
        if context is None:
            context = {}
        res = {}
        for req in self.browse(cr, uid, ids, context=context):
            for cabin in req.departure_id.ship_id.cabin_ids:
                res[cabin.id] = (cabin.max_adult, cabin.max_child)
        return res

    def _read_reservations(self, cr, uid, ids, context=None):
        """Read reservations for departure"""
        if context is None:
            context = {}
        reservations = []
        res = []
        r = []
        for req in self.browse(cr, uid, ids, context=context):
            req_d = []
            req_d.append(req.rq_no)
            reservation_ids = self.search(cr, uid
                    , [('state', 'in', ('request', 'confirm',)),
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
        cabins = []
        totals = {}

        """basic validation. Maximum capacity"""
        for line in res_obj.cruise_reservation_line_ids:
            if not line.cabin_id:
                raise osv.except_osv('Warning', 'Cabin must be setted')
            totals.setdefault(line.cabin_id.id,{'adults':0, 'children':0,
                    'max_adult':0, 'max_child':0})

            totals[line.cabin_id.id]['adults']\
            =totals[line.cabin_id.id]['adults'] + line.adults + line.young
            totals[line.cabin_id.id]['children']\
            =totals[line.cabin_id.id]['children'] + line.children + line.children
            totals[line.cabin_id.id]['max_adult'] = line.cabin_id.max_adult
            totals[line.cabin_id.id]['max_child'] = line.cabin_id.max_child
            cabins.append({'cabin_id':line.cabin_id.id,
                'sharing':line.sharing,'max_adult':line.cabin_id.max_adult,
                     'max_child':line.cabin_id.max_child, 'adults':line.adults,
                     'children':line.children})
            if line.adults + line.young > line.cabin_id.max_adult:
                raise osv.except_osv('Warning'
                , 'Maximum adult capacity reached')
            if line.children > line.cabin_id.max_child:
                raise osv.except_osv('Warning'
                , 'Maximum children capacity reached')
            if line.adults + line.young + line.children <= 0:
                raise osv.except_osv('Warning',
                        'Must set number of passengers in all lines')
        for tk, tv in totals.items():
            if tv['adults'] > tv['max_adult']:
                raise osv.except_osv('Warning',
                        'Maximum capacity of cabin with id {} reached'.format(tk))
        return True

    def _search_departure_cabins(self, cr, uid, ids, context=None):
        """
        male sharing only allows adults
        female sharing only allows adults
        sum of adults, children can't be added not share
        """
        if context is None:
            context = {}

        self_reservation = False

        if self._check_self_reservation(cr,uid,ids[0]):
            self_reservation = True

        return self_reservation

    def _check_cabin_availability(self, values):
        """check cabin availability for current requisition"""
        duplicated = self._find_duplicated(values)

    def _cabins_in_departure(self, cr, uid, _id, context=None):
        """Recover all cabins in departure"""
        request_obj = self.browse(cr, uid, _id, context=context)
        res = {}
        for cabin in request_obj.departure_id.ship_id.cabin_ids:
            res[cabin.id] =\
            {'max_adult':cabin.max_adult,'max_child':cabin.max_child,
             'name':cabin.name}
        return res

    def _read_cabin_availability(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        res = {}
        _all_cabins = self._cabins_in_departure(cr, uid, ids[0], context)

        request_obj = self.browse(cr, uid, ids, context=context)
        departures = {}
        _cabins = {}
        _self_cabins = {}

        for request in request_obj:
            reservation_ids = self.pool.get('cruise.rq').search(cr, uid,
                    ['&', ('departure_id', '=',request.departure_id.id),
                     '&', ('id', '!=', request.id),
                          ('state', 'not in', ['draft', 'wlist', 'cancel'])])
            reservation_obj = self.browse(cr, uid, reservation_ids)
            for reservation in reservation_obj:
                for res_line in reservation.cruise_reservation_line_ids:
                    _cabins.setdefault(res_line.cabin_id.id, {})
                    _cabins[res_line.cabin_id.id][reservation.id] = {
                            'adults':res_line.adults,
                            'sharing':res_line.sharing,
                            'rq_id':reservation.id,
                            'ref':reservation.reference}

        for request in request_obj:
            reservation_ids = self.pool.get('cruise.rq').search(cr, uid,
                    ['&', ('departure_id', '=',request.departure_id.id),
                     '&', ('id', '=', request.id),
                          ('state', 'in', ['draft', 'wlist'])])
            reservation_obj = self.browse(cr, uid, reservation_ids)
            for reservation in reservation_obj:
                for res_line in reservation.cruise_reservation_line_ids:
                    _self_cabins[res_line.cabin_id.id] = {
                            'adults':res_line.adults,
                            'sharing':res_line.sharing,
                            'rq_id':reservation.id}

        skl = [k for k in _self_cabins.keys()]
        ckl = [k for k in _cabins.keys()]
        shared_cabins = {}
        if [v for v in skl if v in ckl]: #Only checks for duplicated cabins
            for sk, sv in _self_cabins.items():
                for ck, cv in _cabins[sk].items():
                    if cv['sharing'] == 'no_sharing':
                        raise osv.except_osv('Warning', 'Already reserved cabin')
                    if cv['sharing'] != sv['sharing']:
                        raise osv.except_osv('Warning'
                                , 'Cabin with {} sharing'.format(cv['sharing']))

                    if cv['sharing'] == sv['sharing']:
                        shared_cabins.setdefault(sk,sv['adults'])
                        shared_cabins[sk] += cv['adults']


        for sk, sv in shared_cabins.items():
            if _all_cabins[sk]['max_adult'] > sv:
                raise osv.except_osv('Warning'
                        , 'Maximum sharing capacity reached')
        return res

    def _cabin_sharing(self, cabins, duplicated):
        """docstring for _cabin_same_sharing"""
        res = {'myid':cabins['myid']}
        for d in duplicated:
            res.setdefault(d, [])
            for c in cabins['cabins']:
                if c['cabin_id'] == d:
                    res[d].append({'rq_id':c['rq_id'], 'sharing':c['sharing']})

        return res

    def _cabin_same_sharing(self, sharing):
        res = {}
        myid = sharing.pop('myid', None)
        mysh = {}
        for cabin_id, sh in sharing.items():
            for s in sh:
                if s['rq_id'] == myid:
                    mysh.setdefault(cabin_id, [])
                    _id = sh.index(s)
                    mysh[cabin_id].append(sh.pop(_id))

        for cabin_id, sh in sharing.items():
            res.setdefault(cabin_id, False)
            lsh = mysh[cabin_id]
            for sl in lsh:
                if s['sharing'] == 'no_sharing':
                    res.setdefault(cabin_id, False)
                    continue
                for s in sh:
                    if s['sharing'] != s['sharing']:
                        res[cabin_id] = False
                    else:
#                        [FIXME] Check capacity
                        res[cabin_id] = True

        return res

    def action_request(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self._read_cabin_availability(cr, uid, ids )
        return self._search_departure_cabins(cr, uid, ids)\
                and self.write(cr, uid, ids, {'state':'request'})\
                or self.write(cr, uid, ids, {'state':'wlist'})

    def action_confirm(self, cr, uid, ids, values, context=None):
        if context is None:
            context = {}
        return self.write(cr, uid, ids, {'state':'confirm'})

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
        'cabin_id':fields.many2one('cruise.cabin', 'Cabin'
            , help='Choose cabin por passenger/s'
            , domain="[('ship_id', '=', line_departure_ship_id)]"),
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

    def onchange_pax(self, cr, uid, ids, ship_id, dummy, context=None):
        pdb.set_trace()
        if context is None:
            context = {}
        print dummy
        print ship_id
        return

    def onchange_cabin(self, cr, uid, ids, cabin_id, context=None):
        pdb.set_trace()
        res = {}
        print cabin_id
        return res


class cruise_cabin(osv.Model):

    '''Inherits cruise.cabin to add m2m relationship with reservation line'''

    _inherit = 'cruise.cabin'

    _columns = {
        'res_ids':fields.many2many('cruise.reservation.line', 'reservation_cabin_rel',
            'cabin_id','rq_line_id','Reservations',
            help='Reservations made to cabin'),

        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
