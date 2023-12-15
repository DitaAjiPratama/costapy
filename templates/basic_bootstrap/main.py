from core   import html
from config import directory

static = [
    {
        'name':'/basic_bootstrap/lib',
        'value':{
            'tools.staticdir.on'    : True ,
            'tools.staticdir.dir'   : './templates/basic_bootstrap/static/lib' ,
        }
    },
    {
        'name':'/basic_bootstrap/css',
        'value':{
            'tools.staticdir.on'    : True ,
            'tools.staticdir.dir'   : './templates/basic_bootstrap/static/css' ,
        }
    }
]

def main(dir, page):

    html_template   = html.main.get_html("templates/basic_bootstrap/html")
    html_page       = html.main.get_html(dir)
    params_list = {
        "template"  : html_template ["template.html"    ]   ,
        "topnav"    : html_template ["topnav.html"      ]   ,
        "footer"    : html_template ["footer.html"      ]   ,
        "container" : html_page     [ page+".html"      ]
    }
    return params_list
