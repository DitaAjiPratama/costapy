import  json
import  requests

def recaptcha(captcha, secret):
    url     = "https://www.google.com/recaptcha/api/siteverify"
    myobj   = {
        "secret"    : secret,
        "response"  : captcha
    }
    response = json.loads(requests.post(url, data = myobj).text)
    return response
