# CostaPy
Python Web Framework. Build with CherryPy and Mako.

## License

CostaPy

Copyright (C) 2022  Dita Aji Pratama

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses/.

## Requirement & Installation

You need this libraries to use CostaPy:
- cherrypy
- cherrypy-cors
- mako
- mysql-connector
- bcrypt
- pyjwt[crypto]

You can install it with run this command

    sh install.sh

Here is the completed command

    sudo apt-get install -y python3-pip
    pip install --upgrade pip
    pip install cherrypy
    pip install cherrypy-cors
    pip install mako
    pip install mysql-connector
    pip install bcrypt
    pip install pyjwt[crypto]

## Usage

Use this command to start the web service

    python<ver> costa.py <ip_address> <port> <service_name>

For an example like this

    python3 costa.py localhost 80 My_Service

You can use nohup too and running it in the background like this

    nohup python3 costa.py localhost 80 My_Service &

## Configuration

### Server (config/server.py)

tools.sessions.on </br>
Default: True </br>
Description: Enable sessions </br>

engine.autoreload.on </br>
Default: False </br>
Description: Auto Reload when source code change. Don't use it in production. </br>

request.show_tracebacks </br>
Default: False </br>
Description: Show traceback for debugging in development purposes. </br>

### Global Variable (config/globalvar.py)

`directory.py` is the place for storing your Global Variable.

GV_base_url </br>
Is the variable for your base URL (without `/` in the end).

GV_title </br>
Is the variable for your web title.

### Directory (config/directory.py)

`directory.py` is the place for storing your path. It is useful to calling the path more efficiently. there is 2 method that you can store your path. store it in variable for templating configuration, and store it as object for routing the url.

This is example that use for templating

    html_user       = "static/pages-user"
    template_user   = "static/template-user"

And this is example that use for routing the url

    dirconfig = {
        '/' :
        {
            'tools.sessions.on'     : True ,
            'tools.staticdir.root'  : os.path.abspath(os.getcwd()) ,
        },
        '/your_dir' :
        {
            'tools.staticdir.on'    : True ,
            'tools.staticdir.dir'   : './static/your-dir' ,
        },
    }

### Templating (config/template.py)

Templating is useful when you had more than 1 website template for difference use case. For an example, when you had user and admin in the use case, the website for user have a navbar and footer, and the website for admin have a navbar and sidebar.

Before you create a template, make sure your `directory` configuration is ready for storing templates and pages. For an example:

    html_user       = "static/pages-user"
    template_user   = "static/template-user"

To create the template, you need to insert this code in `def __init__(self)`

    self.html_pages_user        = html.main.get_html(directory.html_user)
    self.html_template_user     = html.main.get_html(directory.template_user)

if you had admin template, you just need to add the code. for the example like this

    self.html_pages_user        = html.main.get_html(directory.html_user)
    self.html_template_user     = html.main.get_html(directory.template_user)

    self.html_pages_admin       = html.main.get_html(directory.html_admin)
    self.html_template_admin    = html.main.get_html(directory.template_admin)

and then you need create function for each of your template in main class like this

    def user(self, page):
        params_list = {
            "template"  : self.html_template_user        ["user.html"           ]   ,
            "topnav"    : self.html_template_user        ["user-topnav.html"    ]   ,
            "container" : self.html_pages_user           [page+".html"          ]
        }
        return params_list

### Database (config/database.py)

This is the sample template for configure it

    db_default = {
        'host'          : 'localhost',
        'user'          : 'root',
        'password'      : '',
        'database'      : 'your_db',
        'autocommit'    : True,
    }

You also can make more than 1 database configuration like this

    db_default = {
        'host'          : 'localhost',
        'user'          : 'root',
        'password'      : '',
        'database'      : 'your_db',
        'autocommit'    : True,
    }

    db_other = {
        'host'          : 'localhost',
        'user'          : 'root',
        'password'      : '',
        'database'      : 'other_db',
        'autocommit'    : True,
    }

## Handling the modules

Handling the module is in `handler.py`.
