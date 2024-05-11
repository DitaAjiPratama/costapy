# CostaPy
# Copyright (C) 2022 Dita Aji Pratama
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

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
