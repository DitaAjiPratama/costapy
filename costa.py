# CostaPy
# Copyright (C) 2022 Dita Aji Pratama
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

import  sys
from    bottle                  import Bottle, run
from    beaker.middleware       import SessionMiddleware

import  handler

from    core        import staticdir
from    config      import server

app = Bottle()

@app.hook('after_request')
def after_request():
    server.enable_cors()

app.merge(handler.app)
app.merge(staticdir.app)

app = SessionMiddleware(app, server.session_opts)

run(app,
    host = server.host,
    port = server.port,
    reloader = server.reloader,
    server = server.server,
    debug = server.debug
)
