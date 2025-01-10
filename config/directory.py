from core import template

page = {
    'public'    :'pages/public',
    'dashboard' :'pages/dashboard',
    'email'     :'pages/email'
}

static = [
    {
        "route" :"/css/<filepath:re:.*\.(css|sass|css.map)>",
        "root"  :"./static/css"
    },
    {
        "route" :"/js/<filepath:re:.*\.(js)>",
        "root"  :"./static/js"
    }
]
template.add(static, "templates")
