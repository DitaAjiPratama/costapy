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
        APIADDR		= "/api/auth/register/:roles"
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
        APIADDR     = "/api/auth/resend"
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

    def notme(self, params):
        APIADDR         = "/api/auth/notme"
        response        = {}
        loggorilla.prcss(APIADDR, "Define parameters")
        token_encrypt   = params["token"]
        self.cursor.execute("BEGIN;")
        try:
            loggorilla.prcss(APIADDR, "Decrypt token")
            payload = tokenguard.decode(token_encrypt, globalvar.ssh['key']['public'])
            token   = payload['token']
            loggorilla.prcss(APIADDR, "Get dependency data")
            self.cursor.execute(f"SELECT COUNT(*) AS `count`, auth_profile_verification.verified FROM auth_profile_verification INNER JOIN auth_profile ON auth_profile.id = auth_profile_verification.profile WHERE auth_profile.token = %s AND auth_profile_verification.type = 'email' ; ", (token,) )
            result_verification = self.cursor.fetchone()
            self.cursor.execute("SELECT COUNT(*) AS `count`, token, id, email FROM auth_profile WHERE token = %s ; ", (token,) )
            result_profile = self.cursor.fetchone()
            loggorilla.prcss(APIADDR, "Validation")
            if result_verification['verified'] == 1:
                response["status"	] = "failed"
                response["desc"		] = "Your account already verified"
            else:
                loggorilla.prcss(APIADDR, "Deleting")
                self.cursor.execute("DELETE FROM auth WHERE token = %s ; ", (token,) )
                loggorilla.prcss(APIADDR, "Sending email")
                webmail_data 	= {}
                result_webmail	= procedure_webmail.webmail().notme(APIADDR, params, webmail_data)
                self.smtpconfig['to'        ] = result_profile['email'	]
                self.smtpconfig['subject'   ] = result_webmail['subject']
                self.smtpconfig['text'      ] = result_webmail['text'	]
                self.smtpconfig['html'      ] = result_webmail['html'	]
                sendwave.smtp(self.smtpconfig)
                loggorilla.prcss(APIADDR, "Giving response")
                response["status"	] = "success"
                response["desc"		] = "Thanks for your report. Now your data will be deleted from our system."
        except Exception as e:
            self.cursor.execute("ROLLBACK;")
            loggorilla.error(APIADDR, str(e) )
            response["status"		] = "failed"
            response["desc"		] = "Internal Server Error. Please contact us if you still have an error. for detail"
        finally:
            self.cursor.execute("COMMIT;")
            self.cursor.close()
            self.db_main.close()
        return response

    def verify(self, params):
        APIADDR         = "/api/auth/verify"
        response        = {}
        loggorilla.prcss(APIADDR, "Define parameters")
        token_encrypt   = params["token"]
        self.cursor.execute("BEGIN;")
        try:
            loggorilla.prcss(APIADDR, "Decrypt token")
            payload = tokenguard.decode(token_encrypt, globalvar.ssh['key']['public'])
            token   = payload['token']
            expired = datetime.datetime.fromisoformat(payload['expired'])
            loggorilla.prcss(APIADDR, "Get dependency data")
            self.cursor.execute(f"SELECT COUNT(*) AS `count`, auth_profile_verification.verified FROM auth_profile_verification INNER JOIN auth_profile ON auth_profile.id = auth_profile_verification.profile WHERE auth_profile.token = %s AND auth_profile_verification.type = 'email' ; ", (token,) )
            result_verification = self.cursor.fetchone()
            self.cursor.execute("SELECT COUNT(*) AS `count`, token, username, id, email FROM auth_profile WHERE token = %s ; ", (token,) )
            result_profile = self.cursor.fetchone()
            loggorilla.prcss(APIADDR, "Validation")
            if result_verification['verified'] == 1:
                loggorilla.prcss(APIADDR, "Giving response")
                response["status"	] = "failed"
                response["desc"		] = "Your account already verified"
            elif datetime.datetime.now() > expired:
                loggorilla.prcss(APIADDR, "Deleting")
                self.cursor.execute("DELETE FROM `auth` WHERE `token` = %s ; ", (token,) )
                loggorilla.prcss(APIADDR, "Giving response")
                response["status"	] = "failed"
                response["desc"		] = "Expired. Your data removed."
            else:
                loggorilla.prcss(APIADDR, "Updating")
                self.cursor.execute("UPDATE `auth_profile_verification` SET `verified` = 1 WHERE `type` = 'email' AND `profile` = %s ; ", (result_profile['id'],) )
                loggorilla.prcss(APIADDR, "Sending email")
                webmail_data 	= {
                    "username"	: result_profile['username'	],
                    "email"	: result_profile['email'	]
                }
                result_webmail	= procedure_webmail.webmail().welcome(APIADDR, params, webmail_data)
                self.smtpconfig['to'        ] = result_profile['email'	]
                self.smtpconfig['subject'   ] = result_webmail['subject']
                self.smtpconfig['text'      ] = result_webmail['text'	]
                self.smtpconfig['html'      ] = result_webmail['html'	]
                sendwave.smtp(self.smtpconfig)
                loggorilla.prcss(APIADDR, "Giving response")
                response["status"	] = "success"
                response["desc"		] = "Congratulation. Your account is verified."
        except Exception as e:
            self.cursor.execute("ROLLBACK;")
            loggorilla.error(APIADDR, str(e) )
            response["status"	] = "failed"
            response["desc"		] = "Internal Server Error. Please contact us if you still have an error. for detail"
        finally:
            self.cursor.execute("COMMIT;")
            self.cursor.close()
            self.db_main.close()
        return response

    def login(self, params):
        APIADDR     = "/api/auth/login"
        response    = {}
        loggorilla.prcss(APIADDR, "Define parameters")
        username = params["username"].lower()
        password = params["password"]
        self.cursor.execute("BEGIN;")
        try:
            loggorilla.prcss(APIADDR, "Get dependency data")
            self.cursor.execute("SELECT COUNT(*) AS `count`, auth.token, auth_profile.id, auth_profile.username, auth.password FROM auth_profile INNER JOIN auth ON auth.token = auth_profile.token WHERE auth_profile.username = %s ; ", (username,) )
            result_login = self.cursor.fetchone()
            self.cursor.execute("SELECT `profile`, `type`, `verified` FROM auth_profile_verification WHERE `type` = 'email' AND `profile` = %s ; ", (result_login['id'],) )
            result_verification = self.cursor.fetchone()
            loggorilla.prcss(APIADDR, "Validation")
            if result_login['count'] == 1 and result_verification['verified'] == 1 and bcrypt.checkpw(password.encode(), result_login['password'].decode().encode() ) :
                loggorilla.prcss(APIADDR, "Add session")
                self.cursor.execute(f"INSERT INTO `auth_session` VALUES (DEFAULT, %s, NOW(), NOW() + INTERVAL 60 DAY)", ( result_login['token'], ) )
                session_last_id = self.cursor.lastrowid
                self.cursor.execute(f"SELECT `id`, `start`, `end` FROM `auth_session` WHERE id = %s ; ", ( session_last_id, ) )
                session         = self.cursor.fetchone()
                loggorilla.prcss(APIADDR, "Generate JWT token")
                payload         = {
                    "session"   : {
                        "id"        : session['id'      ],
                        "start"     : session['start'   ].isoformat(),
                        "end"       : session['end'     ].isoformat()
                    }
                }
                jwt_token       = tokenguard.encode(payload, globalvar.ssh['key']['private'], globalvar.ssh['passphrase'])
                loggorilla.prcss(APIADDR, "Giving response")
                response["status"   ] = "success"
                response["desc"     ] = "Login success. Session added."
                response["data"     ] = {
                    "jwt"        : jwt_token,
                    "username"   : username
                }
            else:
                response["status"	] = "failed"
                response["desc"		] = "Username or password is incorrect"
        except Exception as e:
            self.cursor.execute("ROLLBACK;")
            loggorilla.error(APIADDR, str(e) )
            response["status"		] = "failed"
            response["desc"		] = "Internal Server Error. Please contact us if you still have an error. for detail"
        finally:
            self.cursor.execute("COMMIT;")
            self.cursor.close()
            self.db_main.close()
        return response

    # Special API for Bottle web session
    def session(self, params):
        APIADDR     = "/api/auth/session/:type"
        loggorilla.prcss(APIADDR, "Define parameters")
        response    = {}
        try:
            type        = params["type" ] # set / check / out
            if type == "set":
                loggorilla.fyinf(APIADDR, "type is 'set': get the jwt from parameters")
                jwt         = params["jwt"  ]
            else:
                loggorilla.fyinf(APIADDR, "type is not 'set': get the jwt from Header")
                loggorilla.prcss(APIADDR, "Extract the token from Header")
                auth_header = request.headers.get('Authorization')
                jwt 	    = auth_header.split(' ')[1]
            payload     	= tokenguard.decode(jwt, globalvar.ssh['key']['public'])
            session_id  	= payload["session"]["id"]
            if type == 'set':
                loggorilla.prcss(APIADDR, "Set authorization on header")
                response.set_header("Authorization", f"Bearer {jwt}")
                response["status"   ] = "success"
                response["desc"     ] = "Session set"
            elif type == 'check':
                loggorilla.prcss(APIADDR, "Check session")
                self.cursor.execute(f"SELECT COUNT(*) AS `count` FROM auth_session WHERE id = %s ; ", (session_id,) )
                result_session = self.cursor.fetchone()
                if result_session == 0:
                    response.set_header("Authorization", "")
                    response["status"   ] = "success"
                    response["desc"     ] = "session out"
                    response["data"     ] = {
                        "status":"lost"
                    }
                else:
                    response["status"   ] = "success"
                    response["desc"     ] = "session active"
                    response["data"     ] = {
                        "status":"active"
                    }
            elif type == 'out':
                loggorilla.prcss(APIADDR, "Remove Authorization header")
                response.set_header("Authorization", "")
                response["status"   ] = "success"
                response["desc"     ] = "Session out"
            else:
                response["status"	] = "failed"
                response["desc"		] = "False parameters"
        except Exception as e:
            loggorilla.error(APIADDR, str(e) )
            response["status"	] = "failed"
            response["desc"		] = "Internal Server Error. Please contact us if you still have an error. for detail"
        finally:
            self.cursor.close()
            self.db_main.close()
        return response

    def forgot(self, params):
        APIADDR     = "/api/auth/forgot"
        response    = {}
        self.cursor.execute("BEGIN;")
        try:
            loggorilla.prcss(APIADDR, "Define parameters")
            email = params["email"].lower()
            loggorilla.prcss(APIADDR, "Get dependency data")
            self.cursor.execute(f"SELECT COUNT(*) AS `count`, auth_profile.token, auth_profile.email FROM auth_profile_verification INNER JOIN auth_profile ON auth_profile.id = auth_profile_verification.profile WHERE auth_profile.email = %s AND auth_profile_verification.type = 'email' AND auth_profile_verification.verified = 1 ; ", (email,) )
            result_verified = self.cursor.fetchone()
            if result_verified["count"] >= 1:
                loggorilla.prcss(APIADDR, "Get token")
                token = result_verified["token"].decode()
                loggorilla.prcss(APIADDR, "Generate URL")
                expired = globalvar.forgot_link_expiration
                expired_isoformat = expired.isoformat()
                payload = {
                    "token" : token,
                    "expired": expired_isoformat
                }
                token_encrypt       = tokenguard.encode(payload, globalvar.ssh['key']['private'], globalvar.ssh['passphrase'])
                change_forgot_url   = globalvar.change_forgot_url(token_encrypt)
                loggorilla.prcss(APIADDR, "Sending email")
                webmail_data 	= {"reset" : change_forgot_url }
                result_webmail	= procedure_webmail.webmail().reset(APIADDR, params, webmail_data)
                self.smtpconfig['to'        ] = email
                self.smtpconfig['subject'   ] = result_webmail['subject']
                self.smtpconfig['text'      ] = result_webmail['text'	]
                self.smtpconfig['html'      ] = result_webmail['html'	]
                sendwave.smtp(self.smtpconfig)
                loggorilla.prcss(APIADDR, "Giving response")
                response["status"	] = "success"
                response["desc"		] = "Check email for reset password."
            else:
                response["status"	] = "failed"
                response["desc"		] = "The parameters seems suspicious and you are not authorized for that"
        except Exception as e:
            self.cursor.execute("ROLLBACK;")
            loggorilla.error(APIADDR, str(e) )
            response["status"	] = "failed"
            response["desc"	] = "Internal Server Error. Please contact us if you still have an error. for detail"
        finally:
            self.cursor.execute("COMMIT;")
            self.cursor.close()
            self.db_main.close()
        return response

    def reset(self, params):
        APIADDR     = "/api/auth/reset"
        response    = {}
        self.cursor.execute("BEGIN;")
        try:
            loggorilla.prcss(APIADDR, "Define parameters")
            token_encrypt   = params["token"    ]
            password        = params["password" ]
            loggorilla.prcss(APIADDR, "Decrypt token")
            payload = tokenguard.decode(token_encrypt, globalvar.ssh['key']['public'])
            token   = payload['token']
            expired = datetime.datetime.fromisoformat(payload['expired'])
            loggorilla.prcss(APIADDR, "Process parameters")
            hashed  = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            loggorilla.prcss(APIADDR, "Get dependency data")
            self.cursor.execute(f"SELECT COUNT(*) AS `count`, auth_profile.email FROM auth_profile_verification INNER JOIN auth_profile ON auth_profile.id = auth_profile_verification.profile WHERE auth_profile.token = %s AND auth_profile_verification.type = 'email' AND auth_profile_verification.verified = 1 ; ", (token,) )
            result_verified = self.cursor.fetchone()
            email = result_verified['email']
            loggorilla.prcss(APIADDR, "Validation")
            if datetime.datetime.now() > expired:
                response["status"	] = "failed"
                response["desc"		] = "Expired"
            elif len(password) < 6:
                response["status"	] = "failed"
                response["desc"		] = "password too short"
            elif result_verified["count"] == 0:
                response["status"	] = "failed"
                response["desc"		] = "Forbidden: No active account for this"
                response["data"     ] = {
                    "message": "Please contact us if you still had a problem"
                }
            else:
                loggorilla.prcss(APIADDR, "Updating")
                self.cursor.execute("UPDATE `auth` SET `password` = %s, `when_update` = NOW() WHERE `token` = %s", (hashed, token) )
                loggorilla.prcss(APIADDR, "Sending email")
                webmail_data 	= {}
                result_webmail	= procedure_webmail.webmail().changed(APIADDR, params, webmail_data)
                self.smtpconfig['to'        ] = email
                self.smtpconfig['subject'   ] = result_webmail['subject']
                self.smtpconfig['text'      ] = result_webmail['text'	]
                self.smtpconfig['html'      ] = result_webmail['html'	]
                sendwave.smtp(self.smtpconfig)
                loggorilla.prcss(APIADDR, "Giving response")
                response["status"	] = "success"
                response["desc"		] = "password change success"
        except Exception as e:
            self.cursor.execute("ROLLBACK;")
            loggorilla.error(APIADDR, str(e) )
            response["status"	] = "failed"
            response["desc"	] = "Internal Server Error. Please contact us if you still have an error. for detail"
        finally:
            self.cursor.execute("COMMIT;")
            self.cursor.close()
            self.db_main.close()
        return response

    def logout(self, params):
        APIADDR     = "/api/auth/logout"
        loggorilla.prcss(APIADDR, "Define parameters")
        response    = {}
        jwt         = params["jwt"  ]
        payload     = tokenguard.decode(jwt, globalvar.ssh['key']['public'])
        session_id  = payload["session"]["id"]
        self.cursor.execute("BEGIN;")
        try:
            loggorilla.prcss(APIADDR, "Deleting")
            self.cursor.execute("DELETE FROM auth_session WHERE id = %s ; ", (session_id,) )
            loggorilla.prcss(APIADDR, "Giving response")
            loggorilla.fyinf(APIADDR, f"Session {session_id} removed.")
            response["status"	] = "success"
            response["desc"	] = f"Your session removed."
        except Exception as e:
            self.cursor.execute("ROLLBACK;")
            loggorilla.error(APIADDR, str(e) )
            response["status"	] = "failed"
            response["desc"	] = "Internal Server Error. Please contact us if you still have an error. for detail"
        finally:
            self.cursor.execute("COMMIT;")
            self.cursor.close()
            self.db_main.close()
        return response

