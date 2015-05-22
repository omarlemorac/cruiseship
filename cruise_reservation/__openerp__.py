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
{
    'name' : 'Cruise Reservation',
    'version' : '0.1',
    'author' : 'Accioma',
    'category' : 'Tour & Travel Operation',
    'description' : """
===============================
Reservation of cruises
===============================
This module allows the managent of reservation for cruises departures.

* Block RQ registration
    A RQ means a non confirmed registration indicating the willing of reserve
    the cruise.

* Reservation.
    In reservation, block status is confirmed and a prepayment is required.

* Confirmation.
    In confirmation full payment is done for the total amount of the reservation.
    After confirmation a service voucher is sended to the customer.

    """,
    'website': 'http://www.accioma.com',
    'images' : [],
    'depends' : [
        'sale','cruiseship','report_webkit'
    ],
    'data': [
        'view/cruise_reservation_view.xml',
        'view/cruiseship_view.xml',
        'sequence/cruise_reservation_seq.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'report/cruise_reservation_report.xml'
    ],
    'js': [
    ],
    'qweb' : [
    ],
    'css':[
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

