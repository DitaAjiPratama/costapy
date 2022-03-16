import  sys
import  os

class main:

    def __init__(self):
        pass

    def get_html(location):
        html_dict = {}
        html_page_list  = os.listdir( location )
        for html_page in html_page_list:
            full_path   = location + "/" + html_page
            html_handle = open( full_path , 'r' )
            html_raw    = html_handle.read()
            html_dict[html_page] = html_raw
        return html_dict
