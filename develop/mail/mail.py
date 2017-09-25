from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from email.header import Header
from email.utils import formatdate

import smtplib
import sys

smtp_obj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
result = smtp_obj.ehlo()
if result[0] != 250:
    print('ehlo is failed.')
    sys.exit()

#result = smtp_obj.starttls()
#if  result[0] != 220:
#    print('starttls is failed.')
#    sys.exit()

# 送信先アドレス，送信アドレスの設定
send_mail = 'haihai.ase@gmail.com'
receive_mail = 'kataoka@pl.info.kochi-tech.ac.jp'

encoding = 'utf-8'

# 件名の設定
subject = 'Caution!!'
# 本文の設定
body = 'A unknown person came out. HAHAHA!!'
# 添付画像のパスの指定
image_pass = '../Server/public/images/photo.jpg'
file_name = 'unknown.jpg'

msg = MIMEMultipart()
mt = MIMEText(body.encode(encoding), "plain", encoding)

img = open(image_pass, 'rb').read()
mj = MIMEImage(img, 'jpeg', filename=file_name)
mj.add_header('Content-Disposition', 'attachment', failname=file_name)
msg.attach(mj)
msg.attach(mt)

msg['Subject'] = Header(subject, encoding)
msg['From'] = send_mail
msg['To'] = receive_mail
msg['Date'] = formatdate()

password = "kataokatakafumi" #input()
result = smtp_obj.login(send_mail, password)
if result[0] != 235:
    print('login is failed.')
    sys.exit()

result = smtp_obj.sendmail(send_mail, [receive_mail], msg.as_string())
if result != {}:
    print('sendmail is failed.')
    sys.exit()
smtp_obj.close()
print('ok')
