from    mako.template       import  Template
import  mysql.connector     as      mariadb

import  config.database		as 		database
import	config.globalvar	as 		globalvar

class main:

	def __init__(self):
 		pass

	def html(self, params):

		interface_template	= params["mako_website"]['template'		]
		topnav				= params["mako_website"]['topnav'		]
		footer				= params["mako_website"]['footer'		]
		container			= params["mako_website"]['container'	]

		name				= "World"

		user_roles			= ["guest"]
		active_page			= "Home"

		return Template(interface_template).render(
			GV_title	= globalvar.GV_title,
			GV_base_url	= globalvar.GV_base_url,
			topnav		= Template(topnav).render(
				GV_title	= globalvar.GV_title,
            	menu		= globalvar.GV_menu['public']['topnav'],
                user_roles	= user_roles,
                active_page	= active_page
			),
			footer		= Template(footer).render(
				copyright_holder	= globalvar.GV_copyright,
			),
            container	= Template(container).render(
				GV_base_url		= globalvar.GV_base_url,
				greeting		= "Hello " + name + ", " + "Welcome to " + globalvar.GV_title
			)
        )
