import datetime

title                   = "Authsquare"
header                  = f"Welcome to {title}"
copyright               = "Copyright (C) 2024  Dita Aji Pratama"

production              = False
forbidden_registration  = ['su', 'admin']

auth_key                = 'your_key'

ssh = {
    "key":{
        "private" : "/root/.ssh/id_rsa",
        "public" : "/root/.ssh/id_rsa.pub"
    },
    "passphrase" : None # use b'value' if use passphrase
}

reCAPTCHA = {
    "client" : "your_key",
    "server" : "your_key"
}

smtpconfig = {
    "login"     : {
        "email"     : "user@domain.com",
        "password"  : "your_password"
    },
    "server"    : {
        "host"      : "smtp.domain.com",
        "port"      : 587
    },
    "from"      : "user@domain.com"
}

verification_link_expiration	= datetime.datetime.now() + datetime.timedelta(minutes=30)
forgot_link_expiration		= datetime.datetime.now() + datetime.timedelta(minutes=30)
# Can be hours or minutes

baseurl     = "https://domain.com"
if production == False:
    baseurl     = "http://localhost:11000"

def resend_url(email):
    url = f"{baseurl}/api/auth/registration/resend?email={email}"
    return url

def notme_url(token):
    url = f"{baseurl}/notme?token={token}"
    return url

def verification_url(token):
    url = f"{baseurl}/verify?token={token}"
    return url

def change_forgot_url(token):
    url = f"{baseurl}/reset?token={token}"
    return url

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
