host        = "localhost"
port        = 15001
reloader    = False
debug       = False
server      = 'gunicorn' # default = 'wsgiref'

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 5*60, # Session expiration in seconds: minutes*seconds
    'session.data_dir': './beaker/data',
    'session.auto': True
}

# cors

# error page 403
# error page 404
# error page 500

# max_request_body_size   = 800 * 1024 * 1024 ,   # Multiply for 800MB result
# socket timeout = 60
# response timeout = 3600
