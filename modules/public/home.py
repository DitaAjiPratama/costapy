from    mako.template		import Template
import	config.globalvar	as globalvar

class main:

    def __init__(self):
        pass

    def html(self, params):
        return Template(params["mako"]["website"]['template']).render(
            title	= globalvar.title,
            baseurl	= globalvar.baseurl,
            topnav	= Template(params["mako"]["website"]['topnav']).render(
                title		= globalvar.title,
                baseurl		= globalvar.baseurl,
                menu		= globalvar.menu['public']['topnav'],
                user_roles	= ["guest"],
                active_page	= "Home"
            ),
            footer	= Template(params["mako"]["website"]['footer']).render(
                copyright	= "Dita Aji Pratama",
            ),
            container	= Template(params["mako"]["website"]['container']).render(
                baseurl		= globalvar.baseurl,
                greeting	= f"Hello world, welcome to {globalvar.title}"
            )
        )
