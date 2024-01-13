import cherrypy
import json
import config.directory		as directory

import templates.bare.main	as bare

import modules.public.home	as public_home

@cherrypy.tools.accept(media="application/json")
class handler():

    def index(self, **kwargs):
        kwargs["mako"] = {
            "website" : bare.main(directory.page["public"], "home")
        }
        return public_home.main().html(kwargs)
    index.exposed = True
