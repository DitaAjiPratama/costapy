# CostaPy
# Copyright (C) 2022 Dita Aji Pratama
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

from    bottle                  import Bottle, route, request, response, redirect
from    config                  import directory

import	json

import  templates.plain.main	as template_public
import  templates.postcard.main	as template_email

import  modules.public.home     as public_home

import  modules.api.auth        as api_auth

app = Bottle()

@app.route('/')
def index():
    params = {
        "mako":{
            "website" : template_public.main(directory.page["public"], "home")
        }
    }
    return public_home.main().html(params)

@app.route('/api/auth/registration/register/<roles>', method=['OPTIONS', 'POST'])
def index(roles):
    try:
        if request.method == 'OPTIONS':
            return None
        else:
            response.content_type = 'application/json'
            params = request.json
            params["roles"  ] = roles
            params["mako"   ] = {
                "email" : template_email.main(directory.page["email"], "verification")
            }
            return json.dumps(api_auth.auth().register(params), indent = 2).encode()
    except Exception as e:
        print(str(e),flush=True)
        return json.dumps({}, indent = 2).encode()

@app.route('/api/auth/registration/resend', method='GET')
def index():
    try:
        if request.method == 'OPTIONS':
            return None
        else:
            response.content_type = 'application/json'
            params = {
                "email" : request.query.email,
                "mako" : {
                    "email" : template_email.main(directory.page["email"], "verification")
                }
            }
            return json.dumps(api_auth.auth().resend(params), indent = 2).encode()
    except Exception as e:
        print(str(e),flush=True)
        return json.dumps({}, indent = 2).encode()
