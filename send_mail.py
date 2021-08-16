import smtplib
from email.mime.text import MIMEText


def send_mail(list_text, mail_server, port, username, password, to_mail):
    msg = ''
    for i in list_text:
        msg += str(i)+ "\n"
    msg = MIMEText('\n {}'.format(msg).encode('utf-8'), _charset='utf-8')
    smtpObj = smtplib.SMTP_SSL(mail_server, port)
    smtpObj.ehlo()
    smtpObj.login(username, password)
    smtpObj.sendmail(username, to_mail, 'Subject: _site_ \n{}'.format(msg))
    smtpObj.quit()

# send_mail(['test1', 'test2'], 'smtp.mail.ru', 465, 'test-70@internet.ru', '6sBPYzGrhLRZmVy1xnJi', ['kotvickiy@inbox.ru', 'vladkotvickiy@gmail.com'])