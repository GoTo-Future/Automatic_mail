import os
import sys
import time
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import email.mime.application
from email import encoders
from platform import python_version
def send_photo(data, *config):
    config = config[0]
    server = config["server"]
    user = config["login"]
    password = config["password"]
    recipients = config['recipients']
    sender = config["name_sender"]
    filepath = config["filepath"]
    print(data)
    for i in recipients:
        msg = MIMEMultipart('alternative')
        msg['From'] = sender + ' <' + user + '>'
        msg['To'] = ', '.join(recipients)
        msg['Reply-To'] = user
        msg['Return-Path'] = user
        msg['X-Mailer'] = 'Python/'+(python_version())#тут можно браузер настроить(наверное
        for i in data:
            try:
                basename = os.path.basename(filepath+i)
                part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(basename))
                f = open(filepath+i,"rb")
                part_file = email.mime.application.MIMEApplication(f.read(),_subtype="jpeg")
                f.close()
                part_file.add_header('Content-Disposition','attachment',filename=filepath+i)
                encoders.encode_base64(part_file)
            except PermissionError:
                continue
        msg.attach(part_file)
        mail = smtplib.SMTP_SSL(server)
        mail.login(user, password)
        mail.sendmail(user, recipients, msg.as_string())
        mail.quit()

if __name__=='__main__':
    with open("config.json") as f:
        config = json.load(f)
    while True:
        directory=os.path.dirname(os.path.abspath(sys.argv[0]))
        dir_list = os.listdir(directory+"/new_data")
        if dir_list != []:
            send_photo(dir_list, config)
            for i in dir_list:
                try:
                    src_path = os.path.join(config['filepath'], i)
                    dst_path = os.path.join(config['file_archive'], i)
                    os.rename(src_path, dst_path)
                except FileExistsError:
                    os.remove(config['filepath']+i)
                except PermissionError:
                    continue
            else:
                pass
        time.sleep(1)