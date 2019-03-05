#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author ZhangYan

import smtplib
from email.mime.text import MIMEText
mailto_list=[]  #收件箱列表
mail_host="smtp.exmail.qq.com"  #设置服务器
mail_user=""    #用户名
mail_pass=""   #客户端授权密码
mail_postfix=""  #发件箱的后缀

def send_mail(sub,content,to_list=mailto_list):
    me="本地部署"+"<"+mail_user.split('@')[0]+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print(str(e))
        return False

