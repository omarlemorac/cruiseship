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
import datetime
class cruise_ship(osv.Model):
    _name = "cruise.ship"
    _description = "Ship"
    _inherit = ['mail.thread']
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

class product_category(osv.osv):
    _inherit = "product.category"
    _columns = {
        'iscabintype':fields.boolean('Is Cabin Type'),
    }
class product_product(osv.osv):
    _inherit = "product.product"
    _columns = {
        'iscabin':fields.boolean('Is Cabin'),
    }

class cabin_type(osv.Model):
    _name='cruise.cabin.type'
    _inherits = {'product.category':'cat_id'}
    _columns = {
        'cat_id':fields.many2one('product.category', 'category', required=True, select=True, ondelete='cascade'),
            }


class cruise_cabin(osv.Model):
    _name = 'cruise.cabin'
    _description = 'Ship cabin'
    _inherit = 'product.product'
    _columns = {
        #'name':fields.char('Name', 255, help='Name', required=True),
        'ship_id':fields.many2one('cruise.ship', 'Ship'),
        'cabin_type_id':fields.many2one('cruise.cabin.type', 'Cruise cabin type'
            , help='Cruise cabin type'),
        'max_adult':fields.integer('Max Adult'),
        'max_child':fields.integer('Max Child'),
        'departure_ids':fields.many2many('cruise.departure'
                , 'departure_cabin_rel'
                , 'departure_id'
                , 'cabin_id'
                , 'Departures'
                , help='Cabins in departure'),
        }
    _defaults = {
        'type':'service',
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
        'departure_cabin_line_id':fields.many2one('departure_cabin.line'
            , 'Departure Cabin Line'
            , help='Departure Cabin Line'),
        'celebration':fields.char('Celebration', 255
            , help='Are you celebrating any special event during your trip?'),
        'accomodation':fields.char('Accomodation', 255
            , help='Hotel accomodation in Ecuador'),
        'tour_company':fields.char('Tour Company', 255
            , help='Tour company providing services in Ecuador'),
        'arriving_flight':fields.char('Arriving Flight', 255
            , help='Please include dates, routing and schedule times (ex: 15MAR MIAUIO 10:15PM)'),
        'departure_flight':fields.char('Departure Flight', 255
            , help='Please include dates, routing and schedule times (ex: 15MAR MIAUIO 10:15PM)'),
        }

class departure_cabin_line(osv.Model):
    _name = 'departure_cabin.line'
    _description = 'Line for cabin in departure'
    _inherits = {'tour_folio.line':'tour_folio_line_id'}


    _columns = {
        'cabin_id':fields.many2one('cruise.cabin', 'Cabin'
           , help='Add a cabin for departure', required=True),
        'tour_folio_line_id':fields.many2one('tour_folio.line', 'Cabin', help='Add a cabin for departure'),
#        'folio_id':fields.many2one('tour.folio', 'Folio'
#        , help='Select asociated Folio',required=True),
        'departure_id':fields.many2one('cruise.departure', 'Departure'
            , help='Departure'),
        'ship_id':fields.related('cabin_id'
            , 'ship_id'
            , readonly=True
            , type='many2one'
            , relation='cruise.ship'
            , string='Ship'
            , help='Ship related to cabin '),
        'state': fields.selection([
               ('draft','Draft')
              ,('wlist','Waiting list')
              ,('request','Request')
              ,('confirm','Confirm')
              ,('cancel','Cancel')
              ]
            , 'State',readonly=True),
        'adult':fields.integer('Bed Space Adult', help='Bed space adult'),
        'children':fields.integer('Bed Space Children', help='Bed space child'),
        'young':fields.integer('Bed Space Young', help='Bed space child'),
        'adult_price_unit':fields.float('Adult price', required=True
            ,digits_compute=dp.get_precision('Product Price')
            ,help='fields help'),
        'young_price_unit':fields.float('Young price', required=True
            ,digits_compute=dp.get_precision('Product Price')
            ,help='fields help'),
        'child_price_unit':fields.float('Child price', required=True
            ,digits_compute=dp.get_precision('Product Price')
            ,help='fields help'),
        'sharing':fields.selection([
            ('male_sharing', 'Male sharing'),
            ('female_sharing', 'Female sharing'),
            ('no_sharing', 'No sharing'),
            ], string='Sharing type', required=True,
            help='Select the sharing type for cabin/s'),
        'confirm_date':fields.related('folio_id'
          , 'confirm_date', type='date', string='Confirm Date'
          , help='Confirm Date'),
        'partner_id':fields.related('folio_id'
          , 'partner_id', type='many2one', string='Customer',relation='res.partner'
          , help='Customer'),
        'user_id':fields.related('folio_id'
          , 'user_id', type='many2one', string='Sales Person',relation='res.users'
          , help='Customer'),
        'cabin_pax_line_ids':fields.one2many('cabin.pax.line'
            , 'departure_cabin_line_id', 'Passenger'
            , help='Add passenger for this departure'),


        }

    _defaults = {
            'state':lambda *a:'draft',
    }
    def _check_cabin_departure(self, cr, uid, ids, context=None):
        cabin_line = self.browse(cr, uid, ids[0], context=context)
        if cabin_line.cabin_id.id not in [c.id for c in
                cabin_line.departure_id.cabin_ids]:
            return False
        return True

    def action_request(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.action_reqconf(cr, uid, ids, 'request', context)

    def action_reqconf(self, cr, uid, ids, target_state, context=None):
        if context is None:
            context = {}
        cabin_line = self.browse(cr, uid, ids[0], context=context)
        cabin_id = cabin_line.cabin_id.id
        reserved = []
        if target_state == 'request':
            reserved = [r.cabin_id for r
                    in cabin_line.departure_id.departure_cabin_line_ids
                    if r.state in ['request', 'confirm']
                      and r.sharing == 'no_sharing']
        if target_state == 'confirm':
            reserved = [r.cabin_id for r
                    in cabin_line.departure_id.departure_cabin_line_ids
                    if r.state in ['confirm']
                      and r.sharing == 'no_sharing']

        #If cabin is already reserved in no_sharing state='wlist'
        if cabin_id in [r.id for r in reserved]:
            return self.write(cr, uid, ids, {'state':'wlist'})

        max_adult = cabin_line.cabin_id.max_adult
        sharing = cabin_line.sharing
        adult = cabin_line.adult

        #If cabin is already reserved an current reservation is no_sharing state='wlist'
        if sharing == 'no_sharing':
            reserved = []
            if target_state == 'request':
                reserved = [r.cabin_id for r
                        in cabin_line.departure_id.departure_cabin_line_ids
                        if r.state in ['request', 'confirm']]
            if target_state == 'confirm':
                reserved = [r.cabin_id for r
                        in cabin_line.departure_id.departure_cabin_line_ids
                        if r.state in ['confirm']]
            if cabin_id in [r.id for r in reserved]:
                return self.write(cr, uid, ids, {'state':'wlist'})
            else:
                return self.write(cr, uid, ids, {'state':target_state})
        else: #Otherwise current reservation is male or female sharing
            #Cabin is reserved with diferent sharing
            reserved = [c.cabin_id.id for c
                    in cabin_line.departure_id.departure_cabin_line_ids
                    if c.state in ['request', 'request']
                      and c.sharing != sharing
                      and c.cabin_id.id == cabin_id]
            if reserved:
                return self.write(cr, uid, ids, {'state':'wlist'})

            #Reserved same sharing
            res_adults = sum([c.adult for c
                    in cabin_line.departure_id.departure_cabin_line_ids
                    if c.state in ['request', 'confirm']
                      and c.sharing == sharing
                      and c.cabin_id.id == cabin_id
                      ])

            if max_adult < res_adults + adult:
                return self.write(cr, uid, ids, {'state':'wlist'})

        return self.write(cr, uid, ids, {'state':target_state})

    def action_confirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.action_reqconf(cr, uid, ids, 'confirm', context)

    def action_cancel(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'cancel'})

    _constraints = [
            (_check_cabin_departure, 'Cabin not available please check Ship/Cabin'
                , ['cabin_id'])
    ]

    def create(self, cr, uid, values, context=None):
        print values
        values['order_id'] = values['folio_id']
        cabin_obj = self.pool.get('product.product')
        departure_obj = self.pool.get('cruise.departure')
        cabin =  cabin_obj.browse(cr, uid, [values['cabin_id']])[0]
        departure = departure_obj.browse(cr,uid,[values['departure_id']])[0]
        dadult = values['adult'] and "{} adult(s) ".format(values['adult']) or ""
        dchildren = values['children'] and "{} child(ren) ".format(values['children']) or ""
        dyoung = values['young'] and "{} young ".format(values['young']) or ""
        description = "{} arrival:{} departure:{}. {} {} {}".format(cabin.name, departure.arrival_date,
                departure.departure_date, dadult, dchildren, dyoung)
        values['name'] = description
        _id = super(departure_cabin_line, self).create(cr,uid,values)
        request = self.action_request(cr, uid, [_id])
        return _id


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
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _order='departure_date'

    def _availability(self, cr, uid, ids, field_name, arg, context=None):
        if context==None:
            context={}
        res = {}
        for dep in self.browse(cr, uid, ids, context):
            av_tot = sum([c.max_adult for c in dep.cabin_ids])
            res[dep.id] = {}
            res[dep.id]['availability'] = av_tot
            request_no_sharing=sum([l.cabin_id.max_adult for l in dep.departure_cabin_line_ids
                if l.state == 'request' and l.sharing=='no_sharing'])
            request_sharing=sum([l.adult + l.young
                for l in dep.departure_cabin_line_ids
                if l.state == 'request' and l.sharing!='no_sharing'])
            res[dep.id]['request'] = request_no_sharing + request_sharing
            confirm_no_sharing=sum([l.cabin_id.max_adult for l in dep.departure_cabin_line_ids
                if l.state == 'confirm' and l.sharing=='no_sharing'])
            confirm_sharing=sum([l.adult + l.young
                for l in dep.departure_cabin_line_ids
                if l.state == 'confirm' and l.sharing!='no_sharing'])
            res[dep.id]['confirm'] = confirm_no_sharing + confirm_sharing
            wlist_no_sharing=sum([l.cabin_id.max_adult for l in dep.departure_cabin_line_ids
                if l.state == 'wlist' and l.sharing=='no_sharing'])
            wlist_sharing=sum([l.adult + l.young
                for l in dep.departure_cabin_line_ids
                if l.state == 'wlist' and l.sharing!='no_sharing'])
            res[dep.id]['wlist'] = wlist_no_sharing + wlist_sharing
            res[dep.id]['available'] = av_tot - (request_no_sharing+
                    request_sharing+confirm_no_sharing+confirm_sharing)


        return res

    def _total_spaces(self, cr, uid, ids, field_name, arg, context=None):
        if context==None:
            context={}
        res = {}
        for dep in self.browse(cr, uid, ids, context):
            res[dep.id] = {}
            res[dep.id]['total_adults'] = 0
            res[dep.id]['total_children'] = 0
            res[dep.id]['total_young'] = 0
            res[dep.id]['total_spaces_taken'] = 0
            for cline in dep.departure_cabin_line_ids:
                if cline.state in ['request', 'confirm']:
                    res[dep.id]['total_adults'] += cline.adult
                    res[dep.id]['total_children'] += cline.children
                    res[dep.id]['total_young'] += cline.young

            res[dep.id]['total_spaces_taken'] = res[dep.id]['total_adults'] +\
                res[dep.id]['total_children'] +\
                res[dep.id]['total_young']


        return res


    _columns = {
        'name':fields.char('Name', 255, help='Name', required=True),
        'departure_date':fields.date('Departure date', help='Departure date',
            required=True),
        'arrival_date':fields.date('Arrival date', help='Arrival date',
            required=True),
        'observations':fields.html('Observations', help='Observations'),
        'ship_id':fields.many2one('cruise.ship', 'Ship',
            help='Add a ship for departure', required=True),
        'itinerary':fields.char('Itinerary', 50, help='Itinerary for this departure '),
        'cabin_ids':fields.many2many('cruise.cabin'
                , 'departure_cabin_rel'
                , 'cabin_id'
                , 'departure_id'
                , 'Cabins'
                , help='Cabins in departure'),

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
        'fast_note':fields.char('Note', 100,
            help='A fast note to briefly inform users'),
        'departure_cabin_line_ids':fields.one2many('departure_cabin.line'
            , 'departure_id'
            , 'Cabins reserved'
            , help='Add cabins reserved'),
        'availability':fields.function(_availability
            , method=True, store=False, type="integer", fnct_search=None
            , multi=True, string='Availability', help='Cabin Availability'),
        'request':fields.function(_availability
            , method=True, store=False, type="integer", fnct_search=None
            , multi=True, string='Request', help='Cabin spaces requested'),
        'confirm':fields.function(_availability
            , method=True, store=False, type="integer", fnct_search=None
            , multi=True, string='Confirm', help='Cabin spaces confirmed'),
        'wlist':fields.function(_availability
            , method=True, store=False, type="integer", fnct_search=None
            , multi=True, string='Waiting List'
            , help='Cabin spaces in waiting list'),
        'available':fields.function(_availability
            , method=True, store=False, type="integer", fnct_search=None
            , multi=True, string='Available', help='Cabin spaces available'),
        'total_adults':fields.function(_total_spaces
            , method=True, store=False, type="integer", fnct_search=None
            , multi=True, string='Total Adults', help='Total adults reserving'),
        'total_children':fields.function(_total_spaces
            , method=True, store=False, type="integer", fnct_search=None
            , multi=True, string='Total Children', help='Total children reserving'),
        'total_young':fields.function(_total_spaces
            , method=True, store=False, type="integer", fnct_search=None
            , multi=True, string='Total Young', help='Total young reserving'),
        'total_spaces_taken':fields.function(_total_spaces
            , method=True, store=False, type="integer", fnct_search=None
            , multi=True, string='Total Spaces Taken', help='Total spaces taken'),
    }

    _defaults = {
        'departure_date':fields.date.context_today,
        'arrival_date': fields.date.context_today,
    }



    def create(self, cr, uid, values, context=None):
        _id = super(departure, self).create(cr,uid,values)
        departure_obj = self.browse(cr,uid,[_id])[0]
        cabins = [(6,0,[cabin.id for cabin in departure_obj.ship_id.cabin_ids])]
        values = {}
        values['cabin_ids'] = cabins
        update_cabins = super(departure, self).write(cr,uid,[_id],values)
        return _id


    def onchange_ship(self, cr, uid, ids, ship_id, departure_date,
            arrival_date, context=None):
        if context is None:
            context = {}
        res = {}
        if ship_id:
            ship_obj = self.pool.get('cruise.ship').browse(cr, uid, ship_id)
            dd = datetime.datetime.strptime(departure_date, '%Y-%m-%d')
            ad = datetime.datetime.strptime(arrival_date, '%Y-%m-%d')

            res['name'] = "{} {}/{}".format(
                           ship_obj.name,dd.strftime('%Y-%b-%d'),
                                         ad.strftime('%b-%d'))
        return {'value':res}

