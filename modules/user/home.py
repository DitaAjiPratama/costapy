import	cherrypy

from    mako.template       import  Template
import  mysql.connector     as      mariadb

import  config.database		as 		database
import	config.globalvar	as 		globalvar

class main:

	def __init__(self):
 		pass

	def html(self, params):

		interface_template	= params["params_page"]['template'	]
		topnav				= params["params_page"]['topnav'	]
		footer				= params["params_page"]['footer'	]
		container			= params["params_page"]['container'	]

		name				= "World"

		return Template(interface_template).render(
			GV_title	= globalvar.GV_title,
			GV_base_url	= globalvar.GV_base_url,
			topnav		= Template(topnav).render(
				GV_title	= globalvar.GV_title,
			),
			footer		= Template(footer).render(
				copyright_holder	= "Dita Aji Pratama",
			),
            container	= Template(container).render(
				GV_base_url		= globalvar.GV_base_url,
				greeting		= "Hello " + name + ", " + "Welcome to " + globalvar.GV_title
			)
        )
