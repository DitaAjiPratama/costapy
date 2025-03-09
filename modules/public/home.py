from    mako.template		import Template
from    config			import globalvar
from    scripts                 import  loggorilla

import  procedure.validation    as 		procedure_validation

class main:

    def __init__(self):
        pass

    def html(self, params):
        APIADDR         = "/"

        loggorilla.prcss(APIADDR, "Define page parameters")
        active_page     = "Home"
        allowed_roles   = [0,1,2,3]

        loggorilla.prcss(APIADDR, "Account validation")
        user_validation = procedure_validation.validation().account(APIADDR, allowed_roles)
        user            = user_validation['data']
        
        return Template(params["mako"]["website"]['index']).render(
            title	= globalvar.title,
            header	= globalvar.header,
            navbar	= Template(params["mako"]["website"]['navbar']).render(
                menu		= globalvar.menu['public']['navbar'],
                user_roles	= user['profile']['roles'],
                active_page	= active_page
            ),
            footer	= Template(params["mako"]["website"]['footer']).render(
                copyright	= globalvar.copyright,
            ),
            container	= Template(params["mako"]["website"]['container']).render(
                greeting	= f"Welcome to your new web application! This placeholder page is here to let you know that your web framework is successfully set up and ready to go. Now, it's time to start building your project. Dive into the documentation to explore the features and capabilities at your disposal."
            )
        )
