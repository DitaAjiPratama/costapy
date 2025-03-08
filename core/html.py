import  os

class main:

    def __init__(self):
        pass

    def get_html(location):
        html_dict = {}
        html_page_list = os.listdir(location)
        for html_page in html_page_list:
            full_path = os.path.join(location, html_page)
            if os.path.isfile(full_path):  # Ensure it's a file, not a directory
                with open(full_path, 'r') as html_handle:
                    html_dict[html_page] = html_handle.read()
        return html_dict
