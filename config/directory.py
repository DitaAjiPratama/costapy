import os

# template import
import templates.basic_bootstrap.main   as basic_bootstrap

# pages directory
page = {
    'public'    :'page/public'  ,
    'error'     :'page/error' # Non-template
}

# public staticdir
dirconfig = {
    '/' :
    {
        'tools.sessions.on'     : True ,
        'tools.staticdir.root'  : os.path.abspath(os.getcwd()) ,
    },
    '/css' :
    {
        'tools.staticdir.on'    : True ,
        'tools.staticdir.dir'   : './static/css' ,
    },
}

def add(template):
    for row in template:
        dirconfig[ row['name'] ] = row['value']

# template staticdir
add(basic_bootstrap.static)
