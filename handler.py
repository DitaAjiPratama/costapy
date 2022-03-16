import cherrypy
import json

import core.authentication      as authentication

import config.globalvar         as globalvar
import config.template          as pages

import modules.user.home        as user_home

class handler(pages.main):

    def __init__(self):
        pages.main.__init__(self)

    def index(self, **kwargs):
        kwargs["params_page"] = pages.main().user("home")
        return user_home.main().html(kwargs)
    index.exposed = True
