import cherrypy
import json
import config.directory                 as directory
import templates.basic_bootstrap.main   as basic_bootstrap
import modules.public.home              as public_home

@cherrypy.tools.accept(media="application/json")
class handler():

    def index(self, **kwargs):
        kwargs["mako_website"] = basic_bootstrap.main(directory.page["public"], "home")
        return public_home.main().html(kwargs)
    index.exposed = True
