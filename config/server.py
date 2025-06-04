from bottle import response

host        = "localhost"
port        = 11000
reloader    = True
debug       = False
server      = 'wsgiref' # try 'gunicorn'

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 5*60, # Session expiration in seconds: minutes*seconds
    'session.data_dir': './.beaker/data',
    'session.auto': True
} # beaker's session options

def enable_cors():
    response.headers['Access-Control-Allow-Origin' ] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, Authorization'

# error page 403
# error page 404
# error page 500

# max_request_body_size   = 800 * 1024 * 1024 ,   # Multiply for 800MB result
# socket timeout = 60
# response timeout = 3600
