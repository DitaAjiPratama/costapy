import  mysql.connector         as      mariadb
from    mako.template           import  Template
from    bottle                  import  request

from    config                  import  database, globalvar

from    scripts                 import  loggorilla, tokenguard

import  procedure.validation    as      procedure_validation

class roles:

    def __init__(self):
        self.db_main    = mariadb.connect(**database.db_main)
        self.cursor     = self.db_main.cursor(dictionary=True)

    def add(self, params):
        APIADDR         = "/api/auth/roles/add"
        response        = {}

        loggorilla.prcss(APIADDR, "Define parameters")
        token           = params["token"    ]
        id              = params["id"       ]
        name            = params["name"     ]
        allowed_roles   = [1]

        loggorilla.prcss(APIADDR, "Account validation")
        user_validation = procedure_validation.validation().account(APIADDR, allowed_roles, token)
        user            = user_validation['data']

        self.cursor.execute("BEGIN;")
        try:
            self.cursor.execute("INSERT INTO `auth_roles` VALUES (%s, %s) ;", (id, name) )
            response["status"   ] = "success"
            response["desc"     ] = "data added"
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

    def list(self, params):
        APIADDR         = "/api/auth/roles/list"
        response        = {}

        loggorilla.prcss(APIADDR, "Define parameters")
        token           = params["token"    ]
        allowed_roles   = [1,2] # Roles list is public or not?

        loggorilla.prcss(APIADDR, "Account validation")
        user_validation = procedure_validation.validation().account(APIADDR, allowed_roles, token)
        user            = user_validation['data']

        self.cursor.execute("BEGIN;")
        try:
            self.cursor.execute("select auth_roles.id, auth_roles.name, (select count(*) from auth_profile_roles apr where apr.roles = auth_roles.id) AS `count` from auth_roles;")
            r_roles = self.cursor.fetchall()
            response["status"   ] = "success"
            response["desc"     ] = "data collected"
            response["data"     ] = r_roles
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

    def edit(self, params):
        APIADDR     = "/api/auth/roles/edit"
        response    = {}

        loggorilla.prcss(APIADDR, "Define parameters")
        token           = params["token"    ]
        key             = params["key"      ]
        id              = params["id"       ]
        name            = params["name"     ]
        allowed_roles   = [1]

        loggorilla.prcss(APIADDR, "Account validation")
        user_validation = procedure_validation.validation().account(APIADDR, allowed_roles, token)
        user            = user_validation['data']

        self.cursor.execute("BEGIN;")
        try:
            if key == 1 or id == 1:
                response["status"	] = "failed"
                response["desc"		] = "Cannot change super user"
            else:
                self.cursor.execute("UPDATE `auth_roles` SET `id` = %s, `name` = %s WHERE `id` = %s ;", (id, name, key) )
                response["status"   ] = "success"
                response["desc"     ] = "data change"
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

    def remove(self, params):
        APIADDR     = "/api/auth/roles/remove"
        response    = {}

        loggorilla.prcss(APIADDR, "Define parameters")
        token           = params["token"    ]
        key             = params["key"      ]
        allowed_roles   = [1]

        loggorilla.prcss(APIADDR, "Account validation")
        user_validation = procedure_validation.validation().account(APIADDR, allowed_roles, token)
        user            = user_validation['data']

        self.cursor.execute("BEGIN;")
        try:
            if key == 1:
                response["status"	] = "failed"
                response["desc"		] = "Cannot change super user"
            else:
                self.cursor.execute("DELETE FROM `auth_roles` WHERE `id` = %s ;", (key,) )
                response["status"   ] = "success"
                response["desc"     ] = "data removed"
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
