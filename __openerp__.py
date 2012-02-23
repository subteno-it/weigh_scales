# -*- coding: utf-8 -*-
##############################################################################
#
#    weigh_scales module for OpenERP, Allow to manage weigh scales from OpenERP
#    Copyright (C) 2012 SYLEAM Info Services (<http://www.Syleam.fr/>)
#              Sylvain Garancher <sylvain.garancher@syleam.fr>
#
#    This file is a part of weigh_scales
#
#    weigh_scales is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    weigh_scales is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Weigh Scales',
    'version': '0.1',
    'category': 'Custom',
    'description': """This module allows to manage weigh scales from OpenERP.

This module needs the "extensions" python module :
$ pip install extension

Weigh scales drivers are managed as plugins by the "extensions" python module.
You can easily add drivers on your system, by registering them in the group 'openerp.addons.weigh_scales.drivers'.
The name of the plugin is the displayed name in OpenERP for the driver.

For example, the CD11 IP driver is registered like this :
register('openerp.addons.weigh_scales.drivers', 'CD11 (IP)', 'weigh_scales.drivers.cd11:cd11_ip')
""",
    'author': 'SYLEAM',
    'website': 'http://www.syleam.fr/',
    'depends': [
        'base',
        'base_tools',
        'product',
    ],
    'init_xml': [],
    'images': [],
    'update_xml': [
        #'security/ir.model.access.csv',
        #'wizard/wizard.xml',
        'weigh_scales_view.xml',
    ],
    'demo_xml': [],
    'test': [],
    'external_dependancies': {
        'python': ['extensions']
    },
    'installable': True,
    'active': False,
    'license': 'AGPL-3',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
