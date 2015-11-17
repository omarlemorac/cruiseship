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

GENDER_LIST = [('m', 'Male'), ('f', 'Female')]

class cruise_ship(models.Model):
    _name = "cruise.ship"
    _description = "Ship"
    _inherit = ['mail.thread']
    name = fields.Char('Ship Name', size=64, required=True, select=True)
    sequence = fields.Integer('Sequence', size=64)
    observations = fields.Html('Observations')
    max_pax = fields.Integer('Maximum capacity'
                             , help='Maximum passenger number allowed in law')
    cabin_ids = fields.One2many('cruise.cabin', 'ship_id', 'Cabins'
                                , help='Add cabins to this ship')
    check_max_capacity = fields.Boolean('Check maximum capacity'
                                        , help='Check maximum capacity in reserving', default=False)



class cabin_pax_line(models.Model):

    '''Pax reserving cabin'''

    _name = 'cabin.pax.line'
    pax_id = fields.Many2one('res.partner', 'Passenger', required=True
        , help='Pax using cabin',
        domain="[('is_pax','=', True)]")
    id_no = fields.Char('Identification Number', required=True
            , help='Identification Number')
    age_ref = fields.Selection([
        ('adult', 'Adult'),
        ('young', 'Young'),
        ('child', 'Child'),
        ]
        , string='Age reference'
        , help='Age reference')
    bed_space_adult = fields.Integer('Bed Space Adult', help='Bed space adult')
    bed_space_child = fields.Integer('Bed Space Child', help='Bed space child')
    departure_cabin_line_id = fields.Many2one('departure_cabin.line'
        , 'Departure Cabin Line'
        , help='Departure Cabin Line')
    celebration = fields.Char('Celebration'
        , help='Are you celebrating any special event during your trip?')
    accomodation = fields.Char('Accomodation'
        , help='Hotel accomodation in Ecuador')
    tour_company = fields.Char('Tour Company'
        , help='Tour company providing services in Ecuador')
    arriving_flight = fields.Char('Arriving Flight'
        , help='Please include dates, routing and schedule times (ex: 15MAR MIAUIO 10:15PM)')
    ib_ap_dep_id = fields.Many2one('touroperation.airport'
        , 'Departure Airport Inbound'
        , help='Select departure airport inbound')
    ib_ap_arr_id = fields.Many2one('touroperation.airport'
        , 'Arrival Airport Inbound'
        , help='Select arrival airport inbound')
    ib_time_dep = fields.Datetime('Departure Inbound Time')
    ib_time_arr = fields.Datetime('Arrival Inbound Time')
    ib_airline_id = fields.Many2one('touroperation.airline'
        , 'Departure Airline Inbound'
        , help='Select inbound departure airline')
    ib_flight_no = fields.Char('Inbound Flight Number'
        , help='Inbound Flight Number')
    ob_ap_dep_id = fields.Many2one('touroperation.airport'
        , 'Departure Airport Outbound'
        , help='Select outbound departure airport')
    ob_ap_arr_id = fields.Many2one('touroperation.airport'
        , 'Arrival Airport Outbound'
        , help='Select arrival airport outbound')
    ob_time_dep = fields.Datetime('Departure Outbound Time')
    ob_time_arr = fields.Datetime('Arrival Outbound Time')
    ob_airline_id = fields.Many2one('touroperation.airline'
        , 'Departure Airline Outbound'
        , help='Select departure outbound airline')
    ob_flight_no = fields.Char('Outbound Flight Number'
        , help='outbound Flight Number')
    arrange_ticket = fields.Boolean('Arrange Ticket?', help='Arrange passenger ticket?')
    arrange_migration_card = fields.Boolean('Arrange Migration Card?',
        help='Arrange passenger migration card?')
    observations = fields.Text('Observations', help='Observations')
    pax_gender = fields.Selection(string='Gender', related = 'pax_id.gender',
                                  help = 'Gender of passenger', readonly = True)
    pax_nationality = fields.Char(string='Nationality', related = 'pax_id.nationality_id.name',
                                      help='Nationality of passenger', readonly = True)
    pax_alle_med = fields.Text(string = 'Allergies / Medical Conditions', related = 'pax_id.allergies_medical',
                               help='Passenger Allergies - Medical conditions')


    @api.onchange('ib_time_dep')
    def onchange_ib_time_dep(self):
        res = {}
        res['value'] = {'ib_time_arr' : self.ib_time_dep}
        return res

    @api.onchange('ob_time_dep')
    def onchange_ob_time_dep(self):
        res = {}
        res['value'] = {'ob_time_arr' : self.ob_time_dep}
        return res

class departure_cabin_line(models.Model):
    _name = 'departure_cabin.line'
    _description = 'Line for cabin in departure'
    _inherits = {'tour_folio.line':'tour_folio_line_id'}

    cabin_id = fields.Many2one('cruise.cabin', 'Cabin'
       , help='Add a cabin for departure', domain=[('iscabin', '=', True)]
       , required=True)
    tour_folio_line_id = fields.Many2one('tour_folio.line', 'Tour Folio Line'
        , help='Tour folio line added in source folio'
        , ondelete='cascade', required = True)
    departure_id = fields.Many2one('cruise.departure', 'Departure'
        , help='Departure')
    ship_id = fields.Many2one(string='Ship', related='cabin_id.ship_id'
        , readonly=True
        , help='Ship related to cabin ')
    state = fields.Selection([
           ('draft', 'Draft')
          ,('wlist', 'Waiting list')
          ,('request', 'Request')
          ,('confirm', 'Confirm')
          ,('cancel', 'Cancel')
          ]
        , 'State', readonly=True, default='draft')
    adult = fields.Integer('Bed Space Adult', help='Bed space adult')
    children = fields.Integer('Bed Space Children', help='Bed space child')
    young = fields.Integer('Bed Space Young', help='Bed space child')
    adult_price_unit = fields.Float('Adult price', required=True
        ,digits_compute=dp.get_precision('Product Price')
        ,help='fields help')
    young_price_unit = fields.Float('Young price', required=True
        ,digits_compute=dp.get_precision('Product Price')
        ,help='fields help')
    child_price_unit = fields.Float('Child price', required=True
        ,digits_compute=dp.get_precision('Product Price')
        ,help='fields help')
    sharing = fields.Selection([
        ('male_sharing', 'Male sharing'),
        ('female_sharing', 'Female sharing'),
        ('no_sharing', 'No sharing'),
        ], string='Sharing type', required=True,
        help='Select the sharing type for cabin/s')
    confirm_date = fields.Date(relation='folio_id.payment_date'
      , string='Confirm Date'
      , help='Confirm Date')
    partner_id = fields.Many2one(string='Customer', relation='res.partner'
      , help='Customer')
    user_id = fields.Many2one(string='Sales Person', relation='res.user'
      , help='Customer')
    cabin_pax_line_ids = fields.One2many('cabin.pax.line'
        , 'departure_cabin_line_id', 'Passenger'
        , help='Add passenger for this departure')

    def _check_cabin_departure(self, cr, uid, ids, context=None):
        cabin_line = self.browse(cr, uid, ids[0], context=context)
        if cabin_line.cabin_id.id not in [c.id for c in
                cabin_line.departure_id.cabin_ids]:
            return False
        return True

    @api.one
    def action_request(self):
        self.action_reqconf('request')

    @api.one
    def action_reqconf(self, target_state):
        cabin_line = self.browse([0])
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
            self.state = 'wlist'
            return

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
                self.state = 'wlist'
                return
            else:
                self.state = target_state
                return
        else: #Otherwise current reservation is male or female sharing
            #Cabin is reserved with diferent sharing
            reserved = [c.cabin_id.id for c
                    in cabin_line.departure_id.departure_cabin_line_ids
                    if c.state in ['request', 'request']
                      and c.sharing != sharing
                      and c.cabin_id.id == cabin_id]
            if reserved:
                self.state = 'wlist'
                return

            #Reserved same sharing
            res_adults = sum([c.adult for c
                    in cabin_line.departure_id.departure_cabin_line_ids
                    if c.state in ['request', 'confirm']
                      and c.sharing == sharing
                      and c.cabin_id.id == cabin_id
                      ])

            if max_adult < res_adults + adult:
                self.state = 'wlist'
                return

        self.state = 'wlist'
        return

    @api.one
    def action_confirm(self):
        self.action_reqconf('confirm')

    def action_cancel(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'cancel'})

    _constraints = [
            (_check_cabin_departure, 'Cabin not available please check Ship/Cabin'
                , ['cabin_id'])
    ]

    def _compute_price_subtotal(self, values):
        return  float(values['adult']) * float(values['adult_price_unit']) + \
                float(values['young']) * float(values['young_price_unit']) + \
                float(values['children']) * float(values['child_price_unit'])

    @api.model
    def create(self, values):
        values['order_id'] = values['folio_id']
        values['price_unit'] = self._compute_price_subtotal(values)
        values['price_subtotal'] = self._compute_price_subtotal(values)
        cabin_obj = self.env['cruise.cabin']
        departure_obj = self.env['cruise.departure']
        cabin =  cabin_obj.browse([values['cabin_id']])[0]
        departure = departure_obj.browse([values['departure_id']])[0]
        dadult = values['adult'] and \
          "{} adult(s) {:.2f}".format(values['adult'], float(values['adult_price_unit'])) or ""
        dchildren = values['children'] and \
          "{} child(ren) {:.2f}".format(values['children'], float(values['child_price_unit'])) or ""
        dyoung = values['young'] and \
          "{} young {:.2f}".format(values['young'], float(values['young_price_unit'])) or ""
        description = "{} {}/{}. {} {} {}".format(cabin.name, departure.arrival_date,
                departure.departure_date, dadult, dchildren, dyoung)
        values['name'] = description
        _id = super(departure_cabin_line, self).create(values)
        print "=============================================="
        print _id
        print "=============================================="
        request = self.action_request()
        return _id


class departure_ship_line(models.Model):

    '''Ships on departure'''

    _name = 'departure.ship.line'

    ship_id = fields.Many2one('cruise.ship', 'Ship', help='Add a ship for departure')
    departure_id = fields.Many2one('cruise.departure', 'Departure'
        , help='Departure')
    max_capacity = fields.Integer(relation='ship_id.max_pax'
        , readonly=True
        , string='Maximum Capacity'
        , help='Maximum capacity of ship')

class departure(models.Model):
    _name = 'cruise.departure'
    _description = 'Cruise Departure'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _order='departure_date'

    @api.one
    @api.depends('cabin_ids', 'departure_cabin_line_ids')
    def _availability(self):
        self.availability = av_tot = sum([c.max_adult for c in self.cabin_ids])

        request_no_sharing=sum([l.cabin_id.max_adult for l in self.departure_cabin_line_ids
            if l.state == 'request' and l.sharing=='no_sharing'])
        request_sharing=sum([l.adult + l.young
            for l in self.departure_cabin_line_ids
            if l.state == 'request' and l.sharing!='no_sharing'])
        self.request = request_no_sharing + request_sharing
        confirm_no_sharing=sum([l.cabin_id.max_adult for l in self.departure_cabin_line_ids
            if l.state == 'confirm' and l.sharing=='no_sharing'])
        confirm_sharing=sum([l.adult + l.young
            for l in self.departure_cabin_line_ids
            if l.state == 'confirm' and l.sharing!='no_sharing'])
        self.confirm = confirm_no_sharing + confirm_sharing
        wlist_no_sharing=sum([l.cabin_id.max_adult for l in self.departure_cabin_line_ids
            if l.state == 'wlist' and l.sharing=='no_sharing'])
        wlist_sharing=sum([l.adult + l.young
            for l in self.departure_cabin_line_ids
            if l.state == 'wlist' and l.sharing!='no_sharing'])

        self.wlist = wlist_no_sharing + wlist_sharing
        self.available = av_tot - (request_no_sharing+
                request_sharing+confirm_no_sharing+confirm_sharing)


    @api.one
    @api.depends('departure_cabin_line_ids')
    def _total_spaces(self):
        self.total_adults = 0
        self.total_children = 0
        self.total_young = 0
        self.total_spaces_taken = 0
        for cline in self.departure_cabin_line_ids:
            if cline.state in ['request', 'confirm']:
                self.total_adults += cline.adult
                self.total_children += cline.children
                self.total_young += cline.young

        self.total_spaces_taken = self.total_adults +\
            self.total_children +\
            self.total_young

    name = fields.Char('Name', help='Name', required=True)
    departure_date = fields.Date('Departure date', help='Departure date',
        required=True, default=fields.Date.today())
    arrival_date = fields.Date('Arrival date', help='Arrival date',
        required=True, default=fields.Date.today())
    observations = fields.Html('Observations', help='Observations')
    ship_id = fields.Many2one('cruise.ship', 'Ship',
        help='Add a ship for departure', required=True)
    itinerary = fields.Char('Itinerary', help='Itinerary for this departure ')
    cabin_ids=fields.Many2many('cruise.cabin'
            , 'departure_cabin_rel'
            , 'cabin_id'
            , 'departure_id'
            , 'Cabins'
            , help='Cabins in departure')
    max_capacity = fields.Integer(string='Maximum Capacity',
          related = 'ship_id.max_pax', readonly=True
        , help='Maximum capacity of ship')
    adult_price_normal = fields.Float('Adult price', required=True
        ,digits_compute=dp.get_precision('Product Price')
        ,help='fields help')
    young_price_normal = fields.Float('Young price', required=True
        ,digits_compute=dp.get_precision('Product Price')
        ,help='fields help')
    child_price_normal = fields.Float('Child price', required=True
        ,digits_compute=dp.get_precision('Product Price')
        ,help='fields help')
    fast_note = fields.Char('Note', size=100,
        help='A fast note to briefly inform users')
    departure_cabin_line_ids = fields.One2many('departure_cabin.line'
        , 'departure_id'
        , 'Cabins reserved'
        , help='Add cabins reserved')
    availability = fields.Integer(compute="_availability"
        , method=True, store=False, fnct_search=None
        , multi=True, string='Availability', help='Cabin Availability')
    request = fields.Integer(compute = "_availability"
        , method=True, store=False, fnct_search=None
        , multi=True, string='Request', help='Cabin spaces requested')
    confirm = fields.Integer(compute = "_availability"
        , method=True, store=False, fnct_search=None
        , string='Confirm', help='Cabin spaces confirmed')
    wlist=fields.Integer(compute="_availability"
        , method=True, store=False, fnct_search=None
        , string='Waiting List'
        , help='Cabin spaces in waiting list')
    available=fields.Integer(compute="_availability"
        , method=True, store=False, fnct_search=None
        , string='Available', help='Cabin spaces available')
    total_adults=fields.Integer(compute="_total_spaces"
        , method=True, store=False,  fnct_search=None
        , string='Total Adults', help='Total adults reserving')
    total_children=fields.Integer(compute="_total_spaces"
        , method=True, store=False, fnct_search=None
        , string='Total Children', help='Total children reserving')
    total_young=fields.Integer(compute="_total_spaces"
        , method=True, store=False, fnct_search=None
        , string='Total Young', help='Total young reserving')
    total_spaces_taken = fields.Integer(compute="_total_spaces"
        , method=True, store=False, fnct_search=None
        , string='Total Spaces Taken', help='Total spaces taken')


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
