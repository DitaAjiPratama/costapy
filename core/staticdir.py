from    bottle      import Bottle, static_file
from    config      import directory

app = Bottle()

for item in directory.static:
    app.route(item['route'], "GET", lambda filepath, root=item['root']: static_file(filepath, root=root) )
