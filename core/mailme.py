from    email.mime.multipart    import MIMEMultipart
from    email.mime.text         import MIMEText
import  smtplib

def smtp(config):

    msg = MIMEMultipart('alternative')
    msg['Subject'   ] = config['subject'    ]
    msg['From'      ] = config['from'       ]
    msg['To'        ] = config['to'         ]

    part1 = MIMEText(config['text'], 'plain')
    part2 = MIMEText(config['html'], 'html' )

    msg.attach(part1)
    msg.attach(part2)

    smtp_server = smtplib.SMTP(config['server']['host'], config['server']['port'])
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login( config['login']['email'], config['login']['password'] )
    smtp_server.sendmail('&&&&&&', email, msg.as_string() )
    smtp_server.quit()
