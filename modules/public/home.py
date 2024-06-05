from    mako.template      import Template
from    config             import globalvar

class main:

    def __init__(self):
        pass

    def html(self, params):
        return Template(params["mako"]["website"]['index']).render(
            title	= globalvar.title,
            header	= "Welcome to CostaPy",
            navbar	= Template(params["mako"]["website"]['navbar']).render(
                menu		= globalvar.menu['public']['navbar'],
                user_roles	= ["guest"],
                active_page	= "Home"
            ),
            footer	= Template(params["mako"]["website"]['footer']).render(
                copyright	= globalvar.copyright,
            ),
            container	= Template(params["mako"]["website"]['container']).render(
                greeting	= f"Welcome to your new web application! This placeholder page is here to let you know that your web framework is successfully set up and ready to go. Now, it's time to start building your project. Dive into the documentation to explore the features and capabilities at your disposal."
            )
        )
