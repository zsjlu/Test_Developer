## 导入SMTP对象，通过help()查看对象的注释，从中找到相关方法说明

- connect(host, port) # 连接服务

- login(user，password）# 登录服务

- sendmail(form_addr, to_addrs, msg,...) # 发送邮件

- quit() # 退出SMTP会话

## 8.2.1 发送HTML格式的邮件

    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    # email模块用来定义邮件的标题和正文

    smtpserver = ''
    
    user = ''

    password = ''

    sender = ''

    receiver = ''
    
    subject = ''

    msg = MIMEText('<html><h1>hello!</h1></html>', 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    # 连接发送邮件

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(user, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

## 8.2.2 发送带附件的邮件

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    smtpserver = ''
    
    user = ''

    password = ''

    sender = ''

    receiver = ''
    
    subject = ''

    sendfile = open('...\\log.txt','rb').read()

    att = MIMEText(sendfile, 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["content-Disposition"] = 'attachment; filename="log.txt"'

    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot.attach(att)

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(user, password)
    smtp.sendmail(sender, receiver, msgRoot.as_string())
    smtp.quit()

## 查找最新的测试报告

    import os

    result_dir = "D:\\testpro\\report"

    lists = os.listdir(result_dir)

    lists.sort(key=lambda fn: os.path.getmtime(result_dir+"\\"+fn))
    # 将匿名函数作为key进行比对

    file = os.path.join(result_dir, lists[-1])

    

    