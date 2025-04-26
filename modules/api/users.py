import  mysql.connector         as      mariadb
from    mako.template           import  Template
from    bottle                  import  request

from    config                  import  database, globalvar

from    scripts                 import  loggorilla, tokenguard

import  procedure.validation    as      procedure_validation

class users:

    def __init__(self):
        self.db_main    = mariadb.connect(**database.db_main)
        self.cursor     = self.db_main.cursor(dictionary=True)

    def list(self, params):
        APIADDR         = "/api/auth/users/list"
        response        = {}

        loggorilla.prcss(APIADDR, "Define parameters")
        token           = params["token"    ]
        allowed_roles   = [1,2]

        loggorilla.prcss(APIADDR, "Account validation")
        user_validation = procedure_validation.validation().account(APIADDR, allowed_roles, token)
        user            = user_validation['data']

        self.cursor.execute("BEGIN;")
        try:
            r_profile = []
            self.cursor.execute("select auth_profile.id, auth_profile.username, auth_profile.email, auth_profile.phone from auth_profile;")
            l1 = self.cursor.fetchall()
            c1 = 0
            for d1 in l1:
                r_profile.append({
                    "id"            : d1["id"       ],
                    "username"      : d1["username" ],
                    "email"         : d1["email"    ],
                    "phone"         : d1["phone"    ],
                    "roles"         : [],
                    "verification"  : []
                })
                self.cursor.execute("select auth_roles.id, auth_roles.name from auth_profile_roles inner join auth_roles on auth_profile_roles.roles = auth_roles.id where auth_profile_roles.profile = %s ; ", ( d1["id"], ) )
                r_profile[c1]["roles"] = self.cursor.fetchall()
                self.cursor.execute("select `type`, `verified` from auth_profile_verification where profile = %s ; ", ( d1["id"], ) )
                r_profile[c1]["verification"] = self.cursor.fetchall()
                c1 += 1
            response["status"   ] = "success"
            response["desc"     ] = "data collected"
            response["data"     ] = r_profile
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
