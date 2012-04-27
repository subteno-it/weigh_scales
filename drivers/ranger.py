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

from common import weigh_scale_ip


class ranger_ip(weigh_scale_ip):
    """
    IP driver for the Ranger series weigh scales
    """

    def __init__(self, hostname, port, timeout=10000):
        """
        Initialize the driver
        """
        super(ranger_ip, self).__init__(hostname, port, timeout=timeout)

    def _get_weight(self):
        """
        Read the current weight on the weigh scale and return a 2-tuple strings (weight, uom_name)
        """
        # Call the weigh scale to get a value
        value = self.send_command('P\r\n')

        if len(value) >= 15 and value[14] != '?':  # and value[15:18] == 'NET':
            # Extract weight and uom name from the returned value
            weight = float(value[2:11])
            if value[0] == '-':
                weight *= -1
            uom_name = value[12:14].strip()

            return (weight, uom_name)

        return None

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
