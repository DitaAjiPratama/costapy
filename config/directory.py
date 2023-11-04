import os

page = {
    'public'    :'page/public'  ,
    'error'     :'page/error' # Non-template
}

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
