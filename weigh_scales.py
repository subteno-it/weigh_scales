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

from osv import osv
from osv import fields
from extensions import get


class weigh_scale(osv.osv):
    _name = 'weigh.scale'
    _description = 'Weigh Scale'

    def _get_types(self, cr, uid, context=None):
        """
        Get all registered types of weigh scales
        """
        types = []

        for type in get(group='openerp.addons.weigh_scales.drivers'):
            types.append((type.name, type.name))

        return sorted(types)

    _columns = {
        'name': fields.char('Name', size=64, required=True, help='Name of the weigh scale'),
        'type': fields.selection(_get_types, 'Type', size=32, required=True, help='Type of printer, used to select the good driver for communication'),
        'hostname': fields.char('Hostname', size=64, required=True, help='Hostname or IP address of the weigh scale'),
        'port': fields.integer('Port', required=True, help='Port of the weigh scale'),
    }

    _defaults = {
         'port': 100,
    }

    def _get_driver(self, cr, uid, weigh_scale, context=None):
        """
        Returns an instance of the driver for the weigh scale parameter
        """
        weigh_scale_type = get(group='openerp.addons.weigh_scales.drivers', name=weigh_scale.type).next().load()
        return weigh_scale_type(weigh_scale.hostname, weigh_scale.port)

    def read_weight(self, cr, uid, ids, context=None):
        """
        Read a weight from weigh scales
        """
        product_uom_obj = self.pool.get('product.uom')
        ret = {}

        for weigh_scale in self.browse(cr, uid, ids, context=context):
            # Retrieve values from the weigh scale
            driver = self._get_driver(cr, uid, weigh_scale, context=context)
            response = driver.read_weight()
            driver.close_connection()

            # Generate return value
            if response is None:
                ret[weigh_scale.id] = None
            else:
                (weight, uom_name) = response
                uom_id = product_uom_obj.name_search(cr, uid, uom_name, context=context, operator='=')[0][0]
                ret[weigh_scale.id] = (weight, uom_id)

        return ret

weigh_scale()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
