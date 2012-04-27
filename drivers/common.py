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

import sys
import socket
import time
import traceback
from datetime import datetime, timedelta
from osv import osv
from tools.translate import _
import logging
logger = logging.getLogger('weigh_scales:common')


class socket_connection(object):
    """
    Common socket communication class
    """

    def __init__(self, hostname, port):
        """
        Initialize the class, connecting to the required hostname on the required port
        """
        self.hostname = hostname
        self.port = port

    def open_connection(self):
        """
        Open a new socket connection, with 5 seconds as default timeout
        """
        self._connection = socket.create_connection((self.hostname, self.port), 5)

    def send_command(self, command):
        """
        Send a command and return its response
        """
        # Try to open connection to the weigh scale, and raise an error if connection fails
        try:
            self.open_connection()
            # TODO : Check if all weigh scales understand the \r terminator, or if we must specify the terminator in each driver
            self._connection.sendall('%s\r' % command)
            response = self._connection.makefile().readline()
            self.close_connection()
        except:
            logger.warning('Exception: %s' % reduce(lambda x, y: x + y, traceback.format_exception(sys.exc_type, sys.exc_value, sys.exc_traceback)))
            raise osv.except_osv(_('Error'), _('Connection to the weigh scale failed.\nPlease check connectivity and configuration.'))

        return response

    def close_connection(self):
        """
        Close the socket connection
        """
        self._connection.close()


class weigh_scale_ip(socket_connection):
    """
    Generic class to manage an IP weigh scale
    """

    def __init__(self, hostname, port, timeout=10000):
        """
        Initialize the driver
        """
        super(weigh_scale_ip, self).__init__(hostname, port)
        self.timeout=timeout

    def read_weight(self):
        """
        Read the current weight on the weigh scale and return a 2-tuple strings (weight, uom_name)
        """
        # Store start date to check timeout
        time_start = datetime.now()
        time_max = time_start + timedelta(milliseconds=self.timeout)

        # Read the value from weigh scale until we get a valid weight
        while True:
            # Check for timeout
            if datetime.now() > time_max:
                return None

            # Call the weigh scale to get a value
            value = self._get_weight()
            if value is not None:
                return value
            else:
                # Wait 200 ms, we don't want to flood the network
                time.sleep(0.5)

    def _get_weight(self):
        """
        Read the current weight on the weigh scale and return a 2-tuple strings (weight, uom_name)
        This method is called by the read_weight method and must be redefined in the subclass for each weigh scale
        """
        raise Exception('This method is not implemented in this object !')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
