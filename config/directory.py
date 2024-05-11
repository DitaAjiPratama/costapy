from core import template

page = {
    'public'    :'pages/public'
}

static = [
    {
        "route" :"/css/<filepath:re:.*\.(css|sass|css.map)>",
        "root"  :"./static/css"
    }
]
template.add(static, "templates")
