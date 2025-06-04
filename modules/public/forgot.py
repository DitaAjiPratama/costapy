from    mako.template           import  Template
from    config                  import  globalvar, navigation
from    scripts                 import  loggorilla

import  procedure.validation    as 		procedure_validation

class forgot:

    def __init__(self):
        pass

    def html(self, params):
        APIADDR         = "/forgot"

        loggorilla.prcss(APIADDR, "Define page parameters")
        active_page     = "Forgot"
        allowed_roles   = [0]

        loggorilla.prcss(APIADDR, "Account validation")
        user_validation = procedure_validation.validation().account(APIADDR, allowed_roles)
        user            = user_validation['data']

        return Template(params["mako"]["website"]['index']).render(
            title	= globalvar.title,
            header	= globalvar.header,
            navbar	= Template(params["mako"]["website"]['navbar']).render(
                menu		= navigation.menu['public']['navbar'],
                user_roles	= user['profile']['roles'],
                active_page	= active_page
            ),
            footer	= Template(params["mako"]["website"]['footer']).render(
                copyright	= globalvar.copyright,
            ),
            container	= Template(params["mako"]["website"]['container']).render()
        )
