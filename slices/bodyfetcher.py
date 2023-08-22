import cherrypy
import cherrypy_cors
import json

def body_json():
    result = None
    if cherrypy.request.method == 'OPTIONS':
        cherrypy_cors.preflight(allowed_methods=['GET', 'POST'])
    if cherrypy.request.method == 'POST':
        cherrypy.serving.response.headers['Content-Type'] = 'application/json'
        body_request = cherrypy.request.body.read()
        result = json.loads(body_request.decode())
    return result
