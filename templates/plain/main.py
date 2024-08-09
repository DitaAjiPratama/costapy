# CostaPy Template - Plain
# Copyright (C) 2024 Dita Aji Pratama
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

from core import html

static = [
    {
        "route"	: "/templates/plain/css/<filepath:re:.*\.(css|sass|css.map)>",
        "root"	: "./templates/plain/static/css"
    }
]

def main(dir, page):
    html_template	= html.main.get_html("templates/plain/html")
    html_page		= html.main.get_html(dir)
    return {
        "index"		: html_template	[ "index.html"	],
        "navbar"	: html_template	[ "navbar.html"	],
        "footer"	: html_template	[ "footer.html"	],
        "container"	: html_page	[f"{page}.html"	]
    }
