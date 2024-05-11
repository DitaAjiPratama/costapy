import  sys
from    bottle      import Bottle, run

import  handler

from    core        import staticdir
from    config      import server

app = Bottle()

app.merge(handler.app)
app.merge(staticdir.app)

run(app,
    host = server.host,
    port = server.port,
    reloader = server.reloader,
    server = server.server,
    debug = server.debug
)
