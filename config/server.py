from config import directory

update = {
    'server.socket_host'                : "hostname"    ,
    'server.socket_port'                : "port"        ,
    'cors.expose.on'                    : True          ,
    'tools.sessions.on'                 : True          ,
    'engine.autoreload.on'              : False         ,
    'request.show_tracebacks'           : False         ,
    'error_page.403'                    : directory.erpadir(403)  ,
    'error_page.404'                    : directory.erpadir(404)  ,
    'error_page.500'                    : directory.erpadir(500)  ,
}
