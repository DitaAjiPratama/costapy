menu        = {
    "public": {
        "navbar": [
            {
                "name":"Home",
                "target":"_self",
                "href":"/",
                "roles":[0,1,2,3]
            },
            {
                "name":"Dashboard",
                "target":"_self",
                "href":"/dashboard",
                "roles":[1,2]
            },
            {
                "name":"Register",
                "target":"_self",
                "href":"/register/member",
                "roles":[0]
            },
            {
                "name":"Login",
                "target":"_self",
                "href":"/login",
                "roles":[0]
            },
            {
                "name":"Logout",
                "target":"_self",
                "href":"/logout",
                "roles":[1,2,3]
            }
        ]
    },
    "dashboard": {
        "navbar": [
            {
                "name":"Home",
                "target":"_self",
                "href":"/",
                "notification":0,
                "roles":[0,1,2,3]
            }
        ],
        "profile": [
            {
                "name"  :"Profile",
                "href"  :"/dashboard/profile",
                "target":"_self",
                "roles":[1,2]
            },
            {
                "name"  :"Settings",
                "href"  :"/dashboard/settings",
                "target":"_self",
                "roles":[1,2]
            },
            {
                "name"  :"Logout",
                "href"  :"/logout",
                "target":"_self",
                "roles":[1,2,3]
            }
        ],
        "sidebar": [
            {
                "icon":"fa-solid fa-gauge",
                "name":"Dashboard",
                "target":"_self",
                "href":"/dashboard",
                "roles":[1,2]
            },
            {
                "icon":"fa-solid fa-user-tag",
                "name":"Roles",
                "target":"_self",
                "href":"/dashboard/roles",
                "roles":[1]
            },
            {
                "icon":"fa-solid fa-address-card",
                "name":"Users",
                "target":"_self",
                "href":"/dashboard/users",
                "roles":[1,2]
            }
        ]
    }
}
