## {{{ http://code.activestate.com/recipes/578472/ (r1)
#!/usr/bin/env python

"""Sending Email in Python

A useful set of functions to facilitate the sending of emails in your Python
application. Supports plain text email body and file attachments complete with
Cc and Bcc support.
"""

from smtplib import SMTP
from itertools import chain
from errno import ECONNREFUSED
from mimetypes import guess_type
from subprocess import Popen, PIPE
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from socket import error as SocketError
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart
from os.path import abspath, basename, expanduser
from sys import argv
from os.path import realpath
from os import uname

def get_mimetype(filename):
    """Returns the MIME type of the given file.

    :param filename: A valid path to a file
    :type filename: str

    :returns: The file's MIME type
    :rtype: tuple
    """

    content_type, encoding = guess_type(filename)
    if content_type is None or encoding is not None:
        content_type = "application/octet-stream"
    return content_type.split("/", 1)


def mimify_file(filename):
    """Returns an appropriate MIME object for the given file.

    :param filename: A valid path to a file
    :type filename: str

    :returns: A MIME object for the givne file
    :rtype: instance of MIMEBase
    """

    filename = abspath(expanduser(filename))
    basefilename = basename(filename)

    msg = MIMEBase(*get_mimetype(filename))
    msg.set_payload(open(filename, "rb").read())
    msg.add_header("Content-Disposition", "attachment", filename=basefilename)

    encode_base64(msg)

    return msg


def send_email(to, subject, text, **params):
    """Send an outgoing email with the given parameters.

    This function assumes your system has a valid MTA (Mail Transfer Agent)
    or local SMTP server. This function will first try a local SMTP server
    and then the system's MTA (/usr/sbin/sendmail) connection refused.

    :param to: A list of recipient email addresses.
    :type to: list

    :param subject: The subject of the email.
    :type subject: str

    :param test: The text of the email.
    :type text: str

    :param params: An optional set of parameters. (See below)
    :type params; dict

    Optional Parameters:
    :cc: A list of Cc email addresses.
    :bcc: A list of Cc email addresses.
    :files: A list of files to attach.
    :sender: A custom sender (From:).
    """

    # Default Parameters
    cc = params.get("cc", [])
    bcc = params.get("bcc", [])
    files = params.get("files", [])
    sender = params.get("sender", "root@localhost")

    recipients = list(chain(to, cc, bcc))

    # Prepare Message
    msg = MIMEMultipart()
    msg.preamble = subject
    msg.add_header("From", sender)
    msg.add_header("Subject", subject)
    msg.add_header("To", ", ".join(to))
    cc and msg.add_header("Cc", ", ".join(cc))

    # Attach the main text
    msg.attach(MIMEText(text))

    # Attach any files
    [msg.attach(mimify_file(filename)) for filename in files]

    # Contact local SMTP server and send Message
    try:
        smtp = SMTP()
        smtp.connect()
        smtp.sendmail(sender, recipients, msg.as_string())
        smtp.quit()
    except SocketError as e:
        if e.args[0] == ECONNREFUSED:
            p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
            p.communicate(msg.as_string())
        else:
            raise

def test():
    # text_str = """
    # asd
    # asd
    # asd
    # asd
    # as
    # das
    # das
    # dasd
    # """
    # file = raw_input('')
    send_email(["chiquete@lanl.gov"], "Test", text_str,sender='chiquete@lanl.gov',
        files=['/home/carlos/work/LANLresearch/DSD_fit/Dnkappa.py'])

def send_email_file(flags_applied):
    to ='chiquete@lanl.gov'
    text = 'Autosent'
    for i,flag in enumerate(flags_applied):
        if (flag[0] == '-'):
            print flag, flags_applied[i+1]
            if ( flag == '-f'):
                file1 = flags_applied[i+1]
            elif ( flag == '-to'):
                to = flags_applied[i+1]
            elif ( flag == '-text'):
                text = flags_applied[i+1]
    send_email([to], 'AUTOSENT: '+file1, text+'\n file : '+realpath(file1) +' \n computer : {} {} {}'.format(*uname()[0:3])
        ,files= [ realpath(file1) ] , sender='chiquete@lanl.gov')

if __name__ == "__main__":
    # test()
    flags_applied = argv[1:]
    # print flags_applied
    send_email_file(flags_applied)

#     if (len(sys.argv) > 1):
#         for flag_var in sys.argv[1:]:
#             for i,flag in enumerate(flags):
#                 if (flag == flag_var):
#                     functions[i](flags_applied)
#     else:
#         print "usage: ./backup.py ",("{} "*len(flags)).format(*flags)
#         for i,flag in enumerate(flags):
#             print '\t {}:'.format(flag),descriptions[i]

## end of http://code.activestate.com/recipes/578472/ }}}