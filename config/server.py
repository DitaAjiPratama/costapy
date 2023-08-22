from config import directory

update = {
    'server.socket_host'                : "hostname"    ,
    'server.socket_port'                : "port"        ,
    'cors.expose.on'                    : True          ,
    'tools.sessions.on'                 : True          ,
    'engine.autoreload.on'              : False         ,
    'request.show_tracebacks'           : False         ,
    'error_page.403'                    : directory.erpadir(403)    ,
    'error_page.404'                    : directory.erpadir(404)    ,
    'error_page.500'                    : directory.erpadir(500)    ,
    'server.max_request_body_size'      : 800 * 1024 * 1024         , # 800MB; Default 100MB
    'server.socket_timeout'             : 60            , # Default 10s
    'response.timeout'                  : 3600          , # Default 300s
}
