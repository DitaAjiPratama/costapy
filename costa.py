# CostaPy
# Copyright (C) 2022 Dita Aji Pratama
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

import sys
import cherrypy
import cherrypy_cors
import handler

from config import server
from config import directory

if __name__ == '__main__':

    dirconfig   = directory.dirconfig
    update      = server.update

    if len(sys.argv) >= 3:

        update["server.socket_host"]    = sys.argv[1]
        update["server.socket_port"]    = int(sys.argv[2])

        cherrypy_cors.install()
        cherrypy.config.update  ( update                                )
        cherrypy.quickstart     ( handler.handler(), config = dirconfig )

    else:
        print ("Usage   : python<ver>   costa.py    <ip_address>    <port>  <service_name>")
        print ("Example : python3       costa.py    localhost       81      CostaPySample")
