from core   import html

static = [
    {
        'name':'/bare/lib',
        'value':{
            'tools.staticdir.on'    : True ,
            'tools.staticdir.dir'   : './templates/bare/static/lib' ,
        }
    },
    {
        'name':'/bare/css',
        'value':{
            'tools.staticdir.on'    : True ,
            'tools.staticdir.dir'   : './templates/bare/static/css' ,
        }
    }
]

def main(dir, page):

    html_template   = html.main.get_html("templates/bare/html")
    html_page       = html.main.get_html(dir)
    params_list = {
        "template"  : html_template ["template.html"    ]   ,
        "topnav"    : html_template ["topnav.html"      ]   ,
        "footer"    : html_template ["footer.html"      ]   ,
        "container" : html_page     [ page+".html"      ]
    }
    return params_list
