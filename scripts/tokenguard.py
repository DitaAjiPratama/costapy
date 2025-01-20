from cryptography.hazmat.primitives import serialization
import jwt

def encode(payload, id_rsa, passphrase):
    private_key = open(id_rsa, 'r').read()
    key         = serialization.load_ssh_private_key(private_key.encode(), password=passphrase)
    token       = jwt.encode(
        payload     = payload,
        key         = key,
        algorithm   = 'RS256'
    )
    return token

def decode(token, id_rsa):
    public_key  = open(id_rsa, 'r').read()
    key         = serialization.load_ssh_public_key(public_key.encode())
    header      = jwt.get_unverified_header(token)
    payload     = jwt.decode(
        jwt         = token,
        key         = key,
        algorithms  = [header['alg'], ]
    )
    return payload
