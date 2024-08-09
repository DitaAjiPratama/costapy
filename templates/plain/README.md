# CostaPy Template - Plain
A plain CostaPy template

## License

CostaPy Template - Plain

Copyright (C) 2024 Dita Aji Pratama

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

## Usage

- Put the folder in your `templates` directory
- Add to handler

		import  templates.plain.main	as template_public

		params["mako"] = {
			"website" : template_public.main(directory.page["public"], "home")
		}

- Define a necessary variable on your modules

		title       = "CostaPy"
		header      = "Welcome to CostaPy"

		user_roles  = ["guest"]
		active_page = "Home"

		copyright   = "Copyright (C) 2022 Dita Aji Pratama"

		greeting    = "Lorem ipsum"

- Define a navbar menu on your modules

		menu = [
			{
				"name":"Home",
				"target":"_self",
				"href":"/",
				"roles":["guest"]
            }
		]

- Set a template on your modules

		return Template(params["mako"]["website"]['index']).render(
			title     = title,
			header    = header,
			navbar    = Template(params["mako"]["website"]['navbar']).render(
				menu        = menu,
				user_roles  = user_roles,
				active_page = active_page
			),
			footer    = Template(params["mako"]["website"]['footer']).render(
				copyright   = copyright,
			),
			container = Template(params["mako"]["website"]['container']).render(
				greeting    = greeting
			)
		)