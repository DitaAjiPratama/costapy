import os
from core import templatestaticdir

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
    '/js' :
    {
        'tools.staticdir.on'    : True ,
        'tools.staticdir.dir'   : './static/js' ,
    },
}

# template staticdir: dirconfig  dirtemplate
templatestaticdir.add(dirconfig, "templates")
