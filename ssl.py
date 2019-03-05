#/usr/bin/env python
#-*- coding:utf-8 -*-
#Authot:Zhang Yan

from subprocess import Popen, PIPE, STDOUT
import time,sys
def CA(ip):
    Popen("touch /etc/pki/CA/index.txt && echo 01 > /etc/pki/CA/serial"
          "&& (umask 077;openssl genrsa -out /etc/pki/CA/private/cakey.pem 2048)",shell=True)
    time.sleep(2)
    p = Popen("openssl req -new -x509 -key /etc/pki/CA/private/cakey.pem -days 7300 -out /etc/pki/CA/cacert.pem",
              shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    p.communicate(input=bytes('CN\nBeijing\nBeijing\ngxb\nops\n%s\n'
                              'yzhang@huikedu.com\n' % ip))
    time.sleep(2)
    Popen("(umask 077;openssl genrsa -out /etc/pki/CA/httpd.key 2048)",shell=True)
    time.sleep(2)
    p = Popen("openssl req -new  -key /etc/pki/CA/httpd.key -days 365 -out /etc/pki/CA/httpd.csr",
              shell = True, stdout = PIPE, stdin = PIPE, stderr = STDOUT)
    p.communicate(input=bytes('CN\nBeijing\nBeijing\ngxb\nops\n%s\n'
                              'yzhang@huikedu.com\n\n\n' % ip))
    time.sleep(2)
    p = Popen("openssl ca -in /etc/pki/CA/httpd.csr -out /etc/pki/CA/httpd.crt -days 365",
              shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    p.communicate(input=bytes('y\ny\n'))
    time.sleep(2)
    Popen("cp -p /etc/pki/CA/httpd.crt /etc/pki/CA/certs/", shell=True)

CA(sys.argv[1])
