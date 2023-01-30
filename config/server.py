def erpadir(err):
    return f'static/error/{err}.html'

update = {
    'server.socket_host'                : "hostname"    ,
    'server.socket_port'                : "port"        ,
    'cors.expose.on'                    : True          ,
    'tools.sessions.on'                 : True          ,
    'engine.autoreload.on'              : False         ,
    'request.show_tracebacks'           : False         ,
    'error_page.403'                    : erpadir(403)  ,
    'error_page.404'                    : erpadir(404)  ,
    'error_page.500'                    : erpadir(500)  ,
}
