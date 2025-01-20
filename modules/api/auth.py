import  mysql.connector     as      mariadb
from    mako.template       import  Template
from    bottle              import  request

from    config              	import  database, globalvar

import  bcrypt
import  datetime

from    scripts             	import loggorilla, saltedkey, googly, tokenguard, sendwave

import  procedure.validation	as procedure_validation
import  procedure.webmail	as procedure_webmail

class auth:

    def __init__(self):
        self.db_main	= mariadb.connect(**database.db_main)
        self.cursor	= self.db_main.cursor(dictionary=True)
        self.smtpconfig	= globalvar.smtpconfig

    def register(self, params):
        APIADDR		= "/api/auth/registration/register/:roles"
        loggorilla.prcss(APIADDR, "Define parameters")
        response	= {}
        captcha		= params["captcha"	]
        username	= params["username"	].lower()
        email		= params["email"	].lower()
        password	= params["password"	]
        roles		= params["roles"	]
        self.cursor.execute("BEGIN;")
        try:
            loggorilla.prcss(APIADDR, "Get dependency data")
            self.cursor.execute(f"SELECT id, name FROM `auth_roles` WHERE auth_roles.name = %s ; ", (roles,) )
            result_roles = self.cursor.fetchone()
            loggorilla.prcss(APIADDR, "Process parameters")
            hashed	= bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            token	= saltedkey.token(username, hashed)
            if globalvar.production == True:
                captcha_r	= googly.recaptcha(captcha, globalvar.reCAPTCHA['server'])
                score		= captcha_r["score"]
            else:
                captcha_r	= 'dev mode'
                score		= 0.9
            loggorilla.fyinf(APIADDR, f'captcha_r : {captcha_r}')
            loggorilla.fyinf(APIADDR, f'score     : {score}')

            loggorilla.prcss(APIADDR, "Validation")
            result_validation = procedure_validation.validation().register(APIADDR, captcha, score, roles, username, password, email)
            if result_validation['status'] == "valid":
                loggorilla.prcss(APIADDR, "Inserting")
                self.cursor.execute("INSERT INTO `auth` VALUES (%s, %s);", (token, hashed) )
                self.cursor.execute("INSERT INTO `auth_profile` VALUES (DEFAULT, %s, %s, %s, NULL);", (token, username, email) )
                auth_profile_lastrowid = self.cursor.lastrowid
                self.cursor.execute("INSERT INTO `auth_profile_verification` VALUES (DEFAULT, %s, 'email', 0);", (auth_profile_lastrowid,) )
                self.cursor.execute("INSERT INTO `auth_profile_roles` VALUES (DEFAULT, %s, %s);", (auth_profile_lastrowid, result_roles['id']) )
                loggorilla.prcss(APIADDR, "Generate URL")
                expired = globalvar.verification_link_expiration
                expired_isoformat = expired.isoformat()
                payload = {
                    "token" : token,
                    "expired": expired_isoformat
                }
                token_encrypt       = tokenguard.encode(payload, globalvar.ssh['key']['private'], globalvar.ssh['passphrase'])
                verification_url    = globalvar.verification_url(token_encrypt)
                notme_url           = globalvar.notme_url(token_encrypt)
                loggorilla.prcss(APIADDR, "Sending email")
                webmail_data 	= {"verify": verification_url, "notme": notme_url}
                result_webmail	= procedure_webmail.webmail().verification(APIADDR, params, webmail_data)
                self.smtpconfig['to'        ] = email
                self.smtpconfig['subject'   ] = result_webmail['subject']
                self.smtpconfig['text'      ] = result_webmail['text'	]
                self.smtpconfig['html'      ] = result_webmail['html'	]
                sendwave.smtp(self.smtpconfig)
                loggorilla.prcss(APIADDR, "Giving response")
                response["status"	] = "success"
                response["desc"		] = "Register success. Check email for verification."
                response["data"     ] = {
                    "recaptcha":captcha_r
                }
            else:
                response = result_validation
        except Exception as e:
            self.cursor.execute("ROLLBACK;")
            loggorilla.error(APIADDR, str(e) )
            response["status"	] = "failed"
            response["desc"	] = "Internal Server Error. Please contact us if you still have an error."
        finally:
            self.cursor.execute("COMMIT;")
            self.cursor.close()
            self.db_main.close()
        return response

    def resend(self, params):
        APIADDR     = "/api/auth/registration/resend"
        loggorilla.prcss(APIADDR, "Define parameters")
        response    = {}
        email       = params["email"].lower()
        try:
            loggorilla.prcss(APIADDR, "Get data for checking")
            self.cursor.execute(f"SELECT COUNT(*) AS `count`, auth_profile.token, auth_profile.email FROM auth_profile_verification INNER JOIN auth_profile ON auth_profile.id = auth_profile_verification.profile WHERE auth_profile.email = %s AND auth_profile_verification.type = 'email' AND auth_profile_verification.verified = 0 ; ", (email,) )
            result_unverified = self.cursor.fetchone()
            token = result_unverified["token"].decode()
            if result_unverified["count"] >= 1:
                loggorilla.prcss(APIADDR, "Generate URL")
                expired = globalvar.verification_link_expiration
                expired_isoformat = expired.isoformat()
                payload = {
                    "token" : token,
                    "expired": expired_isoformat
                }
                token_encrypt       = tokenguard.encode(payload, globalvar.ssh['key']['private'], globalvar.ssh['passphrase'])
                verification_url    = globalvar.verification_url(token_encrypt)
                notme_url           = globalvar.notme_url(token_encrypt)
                loggorilla.prcss(APIADDR, "Sending email")
                webmail_data 	= {"verify": verification_url, "notme": notme_url}
                result_webmail	= procedure_webmail.webmail().verification(APIADDR, params, webmail_data)
                self.smtpconfig['to'        ] = email
                self.smtpconfig['subject'   ] = result_webmail['subject']
                self.smtpconfig['text'      ] = result_webmail['text'	]
                self.smtpconfig['html'      ] = result_webmail['html'	]
                sendwave.smtp(self.smtpconfig)
                loggorilla.prcss(APIADDR, "Giving response")
                response["status"	] = "success"
                response["desc"		] = "Resend success. Check email for verification."
            else:
                response["status"	] = "failed"
                response["desc"		] = "The parameters seems suspicious and you are not authorized for that"
        except Exception as e:
            loggorilla.error(APIADDR, str(e) )
            response["status"	] = "failed"
            response["desc"	] = "Internal Server Error. Please contact us if you still have an error. for detail"
        finally:
            self.cursor.close()
            self.db_main.close()
        return response
