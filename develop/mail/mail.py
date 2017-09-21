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

password = input()
result = smtp_obj.login('send@gmail.com', password)
if result[0] != 235:
    print('login is failed.')
    sys.exit()

result = smtp_obj.sendmail('send@gmail.com', 'receive@gmail.com', 'Subject: test\nThis is a test mail.')
if result != {}:
    print('sendmail is failed.')
    sys.exit()

print('ok')
