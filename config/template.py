from core   import html
from config import directory

class main:

    def __init__(self):
        # Declare a variables
        self.html_page      = html.main.get_html(directory.page)
        self.html_template  = html.main.get_html(directory.template)

    def user(self, page):
        params_list = {
            "template"  : self.html_template    ["template.html"    ]   ,
            "topnav"    : self.html_template    ["topnav.html"      ]   ,
            "footer"    : self.html_template    ["footer.html"      ]   ,
            "container" : self.html_page        [ page+".html"      ]
        }
        return params_list
