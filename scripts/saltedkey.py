import  bcrypt
import  hashlib

def token(username, hashed):
    return hashlib.sha1( (username+username[:3]+hashed[-6:]).encode() ).hexdigest()
