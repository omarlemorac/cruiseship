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
    'name' : 'Cruise Ship Operation',
    'version' : '0.1',
    'author' : 'Accioma',
    'category' : '',
    'description' : """
======================================
Cruise Ship Operation and Management
======================================
This module aims to manage reservations and servces in ordering sales of
ship cruises
    * Cabin configuration
    * Ship departures
    * Availability queries
    * Service voucher
    * Manage of payments
    """,
    'website': 'http://www.accioma.com',
    'images' : [],
    'depends' : [
        "sale"
    ],
    'data': [
        'view/cruiseship_view.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
    ],
    'js': [
    ],
    'qweb' : [
    ],
    'css':[
    ],
    'demo': [
        'demo/ship.xml',
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

