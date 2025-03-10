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
import	modules.public.register	as public_register
import	modules.public.notme	as public_notme
import	modules.public.verify	as public_verify
import	modules.public.login	as public_login
import	modules.public.forgot	as public_forgot
import	modules.public.reset	as public_reset

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

@app.route('/register/<roles>')
def index(roles):
    params = {
        "roles" :roles,
        "mako"  :{
            "website" : template_public.main(directory.page["public"], "register")
        }
    }
    return public_register.register().html(params)

@app.route('/notme', method='GET')
def index():
    params = {
        "mako"  : {
            "website" : template_public.main(directory.page["public"], "notme")
        }
    }
    return public_notme.notme().html(params)

@app.route('/verify', method='GET')
def index():
    params = {
        "mako"  : {
            "website" : template_public.main(directory.page["public"], "verify")
        }
    }
    return public_verify.verify().html(params)

@app.route('/forgot')
def index():
    params = {
        "mako"  : {
            "website" : template_public.main(directory.page["public"], "forgot")
        }
    }
    return public_forgot.forgot().html(params)

@app.route('/reset', method='GET')
def index():
    params = {
        "mako"  : {
            "website" : template_public.main(directory.page["public"], "reset")
        }
    }
    return public_reset.reset().html(params)

@app.route('/login')
def index():
    params = {
        "mako"  : {
            "website" : template_public.main(directory.page["public"], "login")
        }
    }
    return public_login.login().html(params)

@app.route('/logout')
def index():
    beaker_session = request.environ.get('beaker.session')
    if "token" in beaker_session:
        params = {
            "jwt" : beaker_session["token"],
            "type" : "out"
        }
        response_session    = api_auth.auth().session(params)
        response_logout     = api_auth.auth().logout(params)
        if response_session['status'] == 'success' and response_logout['status'] == 'success' :
            redirect('/?message=logout success')
        else:
            print('logout failed')
            print(f"response session: {response_session['status']}")
            print(f"response logout: {response_logout['status']}")
            redirect('/?message=logout failed')
    else:
        redirect('/')

@app.route('/api/auth/register/<roles>', method=['OPTIONS', 'POST'])
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

@app.route('/api/auth/resend', method='GET')
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

@app.route('/api/auth/notme', method=['OPTIONS', 'POST'])
def index():
    try:
        if request.method == 'OPTIONS':
            return None
        else:
            response.content_type = 'application/json'
            params = request.json
            params["mako"   ] = {
                "email" : template_email.main(directory.page["email"], "message")
            }
            return json.dumps(api_auth.auth().notme(params), indent = 2).encode()
    except Exception as e:
        print(str(e),flush=True)
        return json.dumps({}, indent = 2).encode()
    
@app.route('/api/auth/verify', method=['OPTIONS', 'POST'])
def index():
    try:
        if request.method == 'OPTIONS':
            return None
        else:
            response.content_type = 'application/json'
            params = request.json
            params["mako"   ] = {
                "email" : template_email.main(directory.page["email"], "message")
            }
            return json.dumps(api_auth.auth().verify(params), indent = 2).encode()
    except Exception as e:
        print(str(e),flush=True)
        return json.dumps({}, indent = 2).encode()

@app.route('/api/auth/forgot', method=['OPTIONS', 'POST'])
def index():
    try:
        if request.method == 'OPTIONS':
            return None
        else:
            response.content_type = 'application/json'
            params = request.json
            params["mako"   ] = {
                "email" : template_email.main(directory.page["email"], "reset")
            }
            return json.dumps(api_auth.auth().forgot(params), indent = 2).encode()
    except Exception as e:
        print(str(e),flush=True)
        return json.dumps({}, indent = 2).encode()

@app.route('/api/auth/reset', method=['OPTIONS', 'POST'])
def index():
    try:
        if request.method == 'OPTIONS':
            return None
        else:
            response.content_type = 'application/json'
            params = request.json
            params["mako"   ] = {
                "email" : template_email.main(directory.page["email"], "message")
            }
            return json.dumps(api_auth.auth().reset(params), indent = 2).encode()
    except Exception as e:
        print(str(e),flush=True)
        return json.dumps({}, indent = 2).encode()
    
@app.route('/api/auth/login', method=['OPTIONS', 'POST'])
def index():
    try:
        if request.method == 'OPTIONS':
            return None
        else:
            response.content_type = 'application/json'
            params = request.json
            return json.dumps(api_auth.auth().login(params), indent = 2).encode()
    except Exception as e:
        print(str(e),flush=True)
        return json.dumps({}, indent = 2).encode()

@app.route('/api/auth/session/<type>', method=['OPTIONS', 'POST'])
def index(type):
    try:
        if request.method == 'OPTIONS':
            return None
        else:
            response.content_type = 'application/json'
            params = request.json
            params["type"   ] = type
            return json.dumps(api_auth.auth().session(params), indent = 2).encode()
    except Exception as e:
        print(str(e),flush=True)
        return json.dumps({}, indent = 2).encode()

@app.route('/api/auth/logout', method=['OPTIONS', 'POST'])
def index():
    try:
        if request.method == 'OPTIONS':
            return None
        else:
            params = request.json
            return json.dumps(api_auth.auth().logout(params), indent = 2).encode()
    except Exception as e:
        print(str(e),flush=True)
        return json.dumps({}, indent = 2).encode()

