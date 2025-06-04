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

