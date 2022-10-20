import smtplib,time
from email.mime.text import MIMEText
def send_to(rec,content):
    # 设置服务器所需信息
    # 163邮箱服务器地址
    mail_host = 'smtp.163.com'
    # 163用户名
    mail_user = 'ciwardauto'
    # 密码(部分邮箱为授权码)
    mail_pass = 'MIUHQZMFTQSDYIIX'
    # 邮件发送方邮箱地址
    sender = 'ciwardauto@163.com'
    # 邮件接受方邮箱地址，需要[]包裹
    receivers = [rec]


    # 设置email信息
    # 邮件内容设置
    message = MIMEText(content, 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = '新通知'
    # 发送方信息
    message['From'] = 'ciwardauto'
    # 接受方信息
    message['To'] = receivers[0]
    # 登录并发送邮件
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host,25)
    # 登录到服务器
    smtpObj.login(mail_user, mail_pass)
    # 发送
    smtpObj.sendmail(sender, receivers, message.as_string())
    print('Sending successfully!!!')
    # 退出
    smtpObj.quit()

# except smtplib.SMTPException as e:
# print('error',e) #打印错误
