import cherrypy

def token_check(redirect):
    if cherrypy.session.get("token") == None:
        raise cherrypy.HTTPRedirect(redirect)
