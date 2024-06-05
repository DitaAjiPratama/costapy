from    bottle      import Bottle, get, static_file
from    config      import directory

app = Bottle()

for items in directory.static:
    @app.get(items['route'])
    def static_items(filepath):
        return static_file(filepath, root=items['root'])
