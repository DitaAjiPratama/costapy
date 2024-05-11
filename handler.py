from    bottle                  import Bottle, route
from    config                  import directory

import  templates.bare.main     as template_public
import  modules.public.home     as public_home

app = Bottle()

@app.route('/')
def index():
    params = {
        "mako":{
            "website" : template_public.main(directory.page["public"], "home")
        }
    }
    return public_home.main().html(params)
