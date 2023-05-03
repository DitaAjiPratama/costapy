import os

# For templating
page        = "static/page"
template    = "static/template"
email       = "static/email"

# For route
dirconfig = {
    '/' :
    {
        'tools.sessions.on'     : True ,
        'tools.staticdir.root'  : os.path.abspath(os.getcwd()) ,
    },
    '/lib' :
    {
        'tools.staticdir.on'    : True ,
        'tools.staticdir.dir'   : './static/lib' ,
    },
    '/css' :
    {
        'tools.staticdir.on'    : True ,
        'tools.staticdir.dir'   : './static/css' ,
    },
}
