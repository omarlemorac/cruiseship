# -*- coding: utf-8 -*-

from openerp.tests.common import TransactionCase
from datetime import datetime

class GlobalTestResevation(TransactionCase):

    def setUp(self):
        super(GlobalTestResevation, self).setUp()
        self.variable = 'Hello World'
        self.departure = self.env['cruise.departure']
        self.ship = self.env['cruise.ship']

    def create_departure(self, name, departure_date, arrival_date, ship,
            adult_price_normal, young_price_normal, child_price_normal):
        departure_id = self.departure.create({
            'name' : name,
            'departure_date' : departure_date,
            'arrival_date' : arrival_date,
            'ship_id' : ship,
            'adult_price_normal' : adult_price_normal,
            'child_price_normal' : child_price_normal,
            'young_price_normal' : young_price_normal,
            })
        return departure_id

    def create_reservation(self, departure_id, folio_id, cabin_id, adult, children, young,
        sharing, adult_price_unit, young_price_unit, child_price_unit):
        folio = self.env['tour.folio'].browse([folio_id])
        print "Folio name {}".format(folio.name)
        cabin = self.env['cruise.cabin'].browse([cabin_id])
        print "Cabin name {}".format( cabin.name )
        cabin_line = self.env['departure_cabin.line']
        cabin_line_id = cabin_line.create({
            'departure_id' : departure_id,
            'folio_id' : folio_id,
            'cabin_id' : cabin_id,
            'adult' : adult,
            'children' : children,
            'young' : young,
            'sharing' : sharing,
            'adult_price_unit' : adult_price_unit,
            'child_price_unit' : child_price_unit,
            'young_price_unit' : young_price_unit,
            'option_date' : datetime.strptime('2015-11-17', '%Y-%m-%d'),
            'deposit_date' : datetime.strptime('2015-11-20', '%Y-%m-%d'),
            'balance_date' : datetime.strptime('2015-11-25', '%Y-%m-%d'),
        })
        return cabin_line_id

    def test_10_same_gender_sharing(self):
        departure_date = datetime.strptime('2015-11-17', '%Y-%m-%d')
        arrival_date = datetime.strptime('2015-11-24', '%Y-%m-%d')
        name = 'Departure Test'
        print "========================================="
        print "======= Testing Same Gender   ==========="
        ship = self.ship.env.ref("cruiseship.cruise_ship_samba_demo")
        departure_id = self.create_departure(name, departure_date,
                arrival_date, ship.id, 3250.00, 3100.00, 3000.00)
        print "=========================================="
        print "Creada la salida {}".format(departure_id)
        print "=========================================="
        #Create male with one seat reservation
        folio_obj = self.env['tour.folio']
        folio = folio_obj.env.ref('tour_operation.to_folio_01')
        cabin_obj = self.env['cruise.cabin']
        cabin = cabin_obj.env.ref('cruiseship.cruise_ship_cabin_s1_demo')
        #print "Nombre de la cabina {}".cabin.name
        cabin_line_id1 = self.create_reservation(
            departure_id.id,
            folio.id,
            cabin.id,  1, 0, 0,'male_sharing', 1500.00, 1200.00, 1100.00 )
        print "=========================================="
        print "Creada la reserva {} con 1 pax compartido varon".format(cabin_line_id1)
        print "=========================================="

        cabin_line_id1.action_request()
        self.assertEqual(cabin_line_id1.state, 'request')


        cabin_line_id2 = self.create_reservation(
            departure_id.id,
            folio.id,
            cabin.id,  1, 0, 0,'male_sharing', 1500.00, 1200.00, 1100.00 )
        print "=========================================="
        print "Creada la reserva {} con 1 pax compartido varon".format(cabin_line_id2)
        print "=========================================="

        print "=========================================="
        print "La reserva {} deberia estar confirmada".format(cabin_line_id2)
        print "=========================================="

        cabin_line_id2.action_request()

        self.assertEqual(cabin_line_id2.state, 'request')

        cabin_line_id3 = self.create_reservation(
            departure_id.id,
            folio.id,
            cabin.id,  1, 0, 0,'male_sharing', 1500.00, 1200.00, 1100.00 )
        print "=========================================="
        print "Creada la reserva {} con 1 pax compartido varon".format(cabin_line_id3)
        print "=========================================="

        print "=========================================="
        print "La reserva {} deberia estar en lista de espera".format(cabin_line_id3)
        print "=========================================="

        cabin_line_id3.action_request()

        self.assertEqual(cabin_line_id3.state, 'wlist')

        cabin2 = cabin_obj.env.ref('cruiseship.cruise_ship_cabin_s2_demo')
        cabin_line_id4 = self.create_reservation(
            departure_id.id,
            folio.id,
            cabin2.id, 1, 0, 0,'no_sharing', 1500.00, 1200.00, 1100.00 )
        print "=========================================="
        print "Creada la reserva {} no sharing".format(cabin_line_id4)
        print "=========================================="

        print "=========================================="
        print "La reserva {} deberia estar request".format(cabin_line_id4)
        print "=========================================="

        cabin_line_id4.action_request()

        self.assertEqual(cabin_line_id4.state, 'request')
        
    def test_20_no_sharing(self):
        departure_date = datetime.strptime('2015-11-17', '%Y-%m-%d')
        arrival_date = datetime.strptime('2015-11-24', '%Y-%m-%d')
        name = 'Departure Test'
        print "========================================="
        print "======= Testing No sharing    ==========="
        ship = self.ship.env.ref("cruiseship.cruise_ship_samba_demo")
        departure_id = self.create_departure(name, departure_date,
                arrival_date, ship.id, 3250.00, 3100.00, 3000.00)
        print "=========================================="
        print "Departure {} created".format(departure_id)
        print "=========================================="
        #Create male with one seat reservation
        folio_obj = self.env['tour.folio']
        folio = folio_obj.env.ref('tour_operation.to_folio_01')
        cabin_obj = self.env['cruise.cabin']
        cabin = cabin_obj.env.ref('cruiseship.cruise_ship_cabin_s1_demo')
        #print "Nombre de la cabina {}".cabin.name
        cabin_line_id1 = self.create_reservation(
            departure_id.id,
            folio.id,
            cabin.id,  1, 0, 0,'male_sharing', 1500.00, 1200.00, 1100.00 )
        print "=========================================="
        print "Created reservation {} no sharing".format(cabin_line_id1)
        print "=========================================="

        cabin_line_id1.action_request()
        self.assertEqual(cabin_line_id1.state, 'request')