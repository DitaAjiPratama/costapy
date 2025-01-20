import  mysql.connector     as      mariadb
import  datetime
import 	re
from    bottle              import  request, abort, redirect
from    config              import  database, globalvar
from    scripts             import  loggorilla, tokenguard

class validation():

    def __init__(self):
        self.db_main	= mariadb.connect(**database.db_main)
        self.cursor	= self.db_main.cursor(dictionary=True)

    def register(self, APIADDR, captcha, score, roles, username, password, email):
        response={}
        try:
            loggorilla.prcss(APIADDR, "Get the data for checking")
            self.cursor.execute("SELECT COUNT(*) AS `count` FROM auth_profile WHERE email = %s ; ", (email,) )
            result_profile = self.cursor.fetchone()
            self.cursor.execute("SELECT COUNT(*) AS `count` FROM auth_profile WHERE username = %s ; ", (username,) )
            result_username = self.cursor.fetchone()
            self.cursor.execute(f"SELECT COUNT(*) AS `count` FROM auth_profile_verification INNER JOIN auth_profile ON auth_profile.id = auth_profile_verification.profile WHERE auth_profile.email = %s AND auth_profile_verification.type = 'email' AND auth_profile_verification.verified = 0 ; ", (email,) )
            result_unverified = self.cursor.fetchone()
            loggorilla.prcss(APIADDR, "Validating")
            if score < 0.2:
                response["status"	] = "failed"
                response["desc"		] = "you are sus as a bot"
            elif roles in globalvar.forbidden_registration:
                response["status"	] = "failed"
                response["desc"		] = f"Forbidden to become {roles}"
            elif not re.match(r'^\w+$', username):
                response["status"	] = "failed"
                response["desc"		] = "username can only use letters, numbers, and the underscore symbol"
            elif len(username) > 35:
                response["status"	] = "failed"
                response["desc"		] = "username can not longer than 35 character"
            elif len(username) < 3:
                response["status"	] = "failed"
                response["desc"		] = "username too short"
            elif len(password) < 6:
                response["status"	] = "failed"
                response["desc"		] = "password too short"    
            elif result_unverified["count"] >= 1:
                response["status"	] = "failed"
                response["desc"		] = "check email for verification"
                response["data"		] = {
                    "message": "Check email for verification. Please contact us if you still had a problem",
                    "resend": globalvar.resend_url(email)
                }
            elif result_profile["count"] >= 1:
                response["status"	] = "failed"
                response["desc"		] = "email already taken"
            elif result_username["count"] >= 1:
                response["status"	] = "failed"
                response["desc"		] = "username already taken"
            elif not (captcha and username and email and password):
                response["status"	] = "failed"
                response["desc"		] = "Form not complete."
            else:
                response["status"	] = "valid"
                response["desc"		] = "You can continue your register process"
            loggorilla.accss(APIADDR, f"Status      : {response['status']}")
            loggorilla.accss(APIADDR, f"Description : {response['desc'  ]}")
        except Exception as e:
            loggorilla.error(APIADDR, str(e) )
            response["status"	] = "failed"
            response["desc"	] = "Internal Server Error. Please contact us if you still have an error."
        finally:
            self.cursor.close()
            self.db_main.close()
        return response
    
    def account(self, APIADDR, allowed_roles, jwt=None):
        response        = {}
        loggorilla.prcss(APIADDR, "Get jwt")
        if jwt is None:
            loggorilla.fyinf(APIADDR, "jwt params is empty: Use beaker session")
            for_api         = False
            beaker_session  = request.environ.get('beaker.session')
            jwt             = beaker_session["token"] if "token" in beaker_session else None
        else:
            loggorilla.fyinf(APIADDR, "jwt params is available: Use jwt from params")
            for_api         = True
        loggorilla.prcss(APIADDR, "Define parameters")
        if jwt is None:
            loggorilla.fyinf(APIADDR, "Guest")
            r_session = {}
            r_profile = {
                "username"  :None,
                "email"     :None,
                "phone"     :None,
                "roles"     :[0]
            }
            session_not_found   = False
        else:
            loggorilla.fyinf(APIADDR, "With JWT")

            loggorilla.prcss(APIADDR, "Get JWT payload data")
            payload     = tokenguard.decode(jwt, globalvar.ssh['key']['public'])

            loggorilla.prcss(APIADDR, "Connect DB")
            db_main     = mariadb.connect(**database.db_main)
            cursor      = db_main.cursor(dictionary=True)

            loggorilla.prcss(APIADDR, "Get dependency data")

            cursor.execute(f"SELECT * FROM auth_session WHERE id = %s ; ", (payload["session"]["id"],) )
            r_session   = cursor.fetchone()

            if r_session is None:
                session_not_found   = True
                r_session           = {}
                r_profile           = {
                    "username"  :None,
                    "email"     :None,
                    "phone"     :None,
                    "roles"     :[0]
                }
            else:
                session_not_found   = False
                cursor.execute(f"SELECT COUNT(*) AS `count`, auth_profile.* FROM auth_profile_verification LEFT JOIN auth_profile ON auth_profile.id = auth_profile_verification.profile WHERE auth_profile.token = %s AND auth_profile_verification.type = 'email' AND auth_profile_verification.verified = 1 ; ", (r_session['token'],) )
                r_profile           = cursor.fetchone()
                cursor.execute(f"SELECT auth_roles FROM auth_profile_roles WHERE auth_profile = %s ; ", (r_profile['id'],) )
                r_roles             = cursor.fetchall()
                r_profile['roles']  = [item['auth_roles'] for item in r_roles]

            loggorilla.prcss(APIADDR, "Close DB")
            cursor.close()
            db_main.close()

        loggorilla.accss(APIADDR, f"Session ID          : {r_session['id'       ]                               if 'id'         in r_session else None}" )
        loggorilla.accss(APIADDR, f"Session Start       : {r_session['start'    ].strftime('%Y-%m-%d %H:%M:%S') if 'start'      in r_session else None}" )
        loggorilla.accss(APIADDR, f"Session End         : {r_session['end'      ].strftime('%Y-%m-%d %H:%M:%S') if 'end'        in r_session else None}" )
        loggorilla.accss(APIADDR, f"Profile ID          : {r_profile['id'       ]                               if 'id'         in r_profile else None}" )
        loggorilla.accss(APIADDR, f"Profile Username    : {r_profile['username' ]                               if 'username'   in r_profile else None}" )
        loggorilla.accss(APIADDR, f"Profile Email       : {r_profile['email'    ]                               if 'email'      in r_profile else None}" )
        loggorilla.accss(APIADDR, f"Profile Phone       : {r_profile['phone'    ]                               if 'phone'      in r_profile else None}" )
        loggorilla.accss(APIADDR, f"Profile Roles       : {r_profile['roles'    ]                               if 'roles'      in r_profile else None}" )

        loggorilla.prcss(APIADDR, "Validation")
        if session_not_found:
            loggorilla.accss(APIADDR, "Session not found" )
            loggorilla.prcss(APIADDR, "Giving response")
            response["status"	] = "failed"
            response["desc"		] = "Your session not found."
            response["data"		] = {
                "token"     : jwt,
                "valid"     :{
                    "status"    : 0,
                    "desc"      : "removed"
                },
                "session"   : r_session,
                "profile"   : r_profile
            }
            if for_api is True:
                abort(401, "Session not found")
            else:
                redirect('/logout?msg=removed')
        elif 0 not in r_profile['roles'] and datetime.datetime.now() > r_session['end']:
            loggorilla.accss(APIADDR, "Session expired" )
            loggorilla.prcss(APIADDR, "Deleting session")
            self.cursor.execute("DELETE FROM auth_session WHERE id = %s ; ", (r_session['id'],) )
            loggorilla.prcss(APIADDR, "Giving response")
            response["status"	] = "failed"
            response["desc"		] = "Expired. Your session removed."
            response["data"		] = {
                "token"     : jwt,
                "valid"     :{
                    "status"    : 0,
                    "desc"      : "expired"
                },
                "session"   : r_session,
                "profile"   : r_profile
            }
            if for_api is True:
                abort(401, "Session expired")
            else:
                redirect('/logout?msg=expired')
        elif 0 not in r_profile['roles'] and r_profile["count"] == 0:
            loggorilla.accss(APIADDR, "No active account for this" )
            loggorilla.prcss(APIADDR, "Giving response")
            response["status"	] = "failed"
            response["desc"		] = "No active account for this"
            response["data"		] = {
                "token"     : jwt,
                "message"   : "Please contact us if you still had a problem",
                "valid"     :{
                    "status"    : 0,
                    "desc"      : "fake"
                },
                "session"   : r_session,
                "profile"   : r_profile
            }
            abort(403, "Please contact us if you still had a problem.") # 403 Forbidden
        elif any(role in allowed_roles for role in r_profile['roles']):
            loggorilla.accss(APIADDR, "User roles authorized" )
            loggorilla.prcss(APIADDR, "Giving response")
            response["status"	] = "success"
            response["desc"		] = "User roles authorized"
            response["data"		] = {
                "token"     : str(jwt),
                "valid"     :{
                    "status"    : 1,
                    "desc"      : "authorized"
                },
                "session"   : r_session,
                "profile"   : r_profile
            }
            return response
        else:
            loggorilla.accss(APIADDR, "User roles unauthorized" )
            loggorilla.prcss(APIADDR, "Giving response")
            response["status"	] = "failed"
            response["desc"		] = "User roles unauthorized"
            response["data"		] = {
                "token"     : jwt,
                "valid"     :{
                    "status"    : 0,
                    "desc"      : "unauthorized"
                },
                "session"   : r_session,
                "profile"   : r_profile
            }
            abort(401, "User roles unauthorized") # 401 Unauthorized
