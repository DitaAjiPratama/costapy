from mako.template import Template
from config import globalvar

class webmail():

    def __init__(self):
        pass

    def verification(self, APIADDR, params, data):
        return {
            "subject"	: f"{globalvar.title} email verification",
            "text"	: f"Please visit this link to complete the registration: {data['verify']} . You are not registering this? report on this: {data['notme']} .",
            "html"	: Template(params["mako"]["email"]['index']).render(
                title       = globalvar.title,
                header      = globalvar.title,
                copyright   = globalvar.copyright,
                container = Template(params["mako"]["email"]['container']).render(
                    header  = "One more step to complete your registration!",
                    verify  = data['verify'	],
                    notme   = data['notme'	]
                )
            )
        }

    def notme(self, APIADDR, params, data):
        return {
            "subject"	: f"{globalvar.title} - Thanks for the reporting",
            "text"	: "Thanks for your report. Now your data will be deleted from our system.",
            "html"	: Template(params["mako"]["email"]['index']).render(
                title       = globalvar.title,
                header      = globalvar.title,
                copyright   = globalvar.copyright,
                container = Template(params["mako"]["email"]['container']).render(
                        message = "Thanks for your report. Now your data will be deleted from our system."
                )
            )
        }

    def welcome(self, APIADDR, params, data):
        return {
            "subject"	: f"Welcome to {globalvar.title}",
            "text"	: f"Welcome {data['username']}, Now your account is verified.",
            "html"	: Template(params["mako"]["email"]['index']).render(
                title       = globalvar.title,
                header      = globalvar.title,
                copyright   = globalvar.copyright,
                container   = Template(params["mako"]["email"]['container']).render(
                    message = f"Welcome {data['username']}, Now your account is verified."
        	)
            )
        }

    def reset(self, APIADDR, params, data):
        return {
            "subject"	: f"{globalvar.title} - Reset password",
            "text"	: f"Please visit this link to reset password: {data['reset']}. Avoid the link if you are not request this.",
            "html"	: Template(params["mako"]["email"]['index']).render(
                title       = globalvar.title,
                header      = globalvar.title,
                copyright   = globalvar.copyright,
                container   = Template(params["mako"]["email"]['container']).render(
                    reset   = data['reset']
                )
            )
        }

    def changed(self, APIADDR, params, data):
        return {
            "subject"	: f"{globalvar.title} - password change success",
            "text"	: "You had change your password.",
            "html"	: Template(params["mako"]["email"]['index']).render(
                title       = globalvar.title,
                header      = globalvar.title,
                copyright   = globalvar.copyright,
                container   = Template(params["mako"]["email"]['container']).render(
                    message = "You had change your password."
                )
            )
        }
