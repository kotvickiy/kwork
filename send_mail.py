import smtplib
from email.mime.text import MIMEText


def send_mail(list_text,
              to_mail=['test-70@internet.ru'],
              mail_server='smtp.mail.ru',
              port=465,
              username='test-70@internet.ru',
              password='6sBPYzGrhLRZmVy1xnJi'):
    msg = ''
    for i in list_text:
        msg += str(i)+ "\n"
    msg = MIMEText('\n {}'.format(msg).encode('utf-8'), _charset='utf-8')
    smtpObj = smtplib.SMTP_SSL(mail_server, port)
    smtpObj.ehlo()
    smtpObj.login(username, password)
    smtpObj.sendmail(username, to_mail, 'Subject: _site_ \n{}'.format(msg))
    smtpObj.quit()
