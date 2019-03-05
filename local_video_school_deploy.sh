#!/bin/bash
rpm=/bin/rpm
yum=/usr/bin/yum
sed=/bin/sed
CA_DIR=/etc/pki/CA
[ ! -f RPM-GPG-KEY-GXB -a -f rpm-gpg-key-gxb ] && mv rpm-gpg-key-gxb  RPM-GPG-KEY-GXB
echo -n  "please input your school_id: "
read school_id
echo -n  "please input your ip: "
read ip
pids=`ps aux|grep -E '(httpd|nginx|deploy_school|deploy_course)'|grep -v grep|awk '{print $2}'`
[ -z "$pids" ] || kill -9 $pids
rpms=`rpm -qa|grep -E '(httpd|nginx|localvideodeploy|videolocaldeploy)'` && rpm -e --nodeps $rpms
[ -f RPM-GPG-KEY-GXB ] && rpm --import RPM-GPG-KEY-GXB
rpm -q epel-release &> /dev/null || rpm -ivh epel-release-6-8.noarch.rpm &> /dev/null
rpm -q wget &> /dev/null || yum -y install wget &> /dev/null
sed -i 's/^#baseurl/baseurl/g;s/^mirrorlist/#mirrorlist/g' /etc/yum.repos.d/epel.repo
yum install -y localvideodeploy-1.4.2-1.el6.x86_64.rpm &> /dev/null
#如果是https，而且没有购买证书需要自签名证书的话执行
#python ssl.py $ip
#if [ -z "`grep $ip ${CA_DIR}/index.txt`" ];then
#        echo "Certificate generation failed!"
#        exit
#fi
#cp -f /etc/pki/CA/httpd.crt /home/kkb/nginx/conf/
#cp -f /etc/pki/CA/httpd.key /home/kkb/nginx/conf/
sed -i "s/server_name 192.168.30.9/server_name $ip/g" /home/kkb/nginx/conf/nginx.conf
chown -R kkb.kkb /home/kkb/
/home/kkb/nginx/sbin/nginx -s reload
sed -i "s/school_id = .*/school_id = ${school_id}/" /home/kkb/videolocaldeploy/conf/setting.conf
[ -f /var/spool/cron/kkb ] && /bin/rm -rf /var/spool/cron/kkb || umask 0177 ; /bin/touch /var/spool/cron/kkb ; /bin/chown kkb:kkb /var/spool/cron/kkb
sed -i '/videolocaldeploy/d' /var/spool/cron/kkb
echo '0 1 * * * /usr/bin/python /home/kkb/videolocaldeploy/deploy_school.py &> /home/kkb/videolocaldeploy/log/$(date "+\%Y-\%m-\%d").log &' >> /var/spool/cron/kkb
echo '0 0 * * * /bin/find /home/kkb/videolocaldeploy/log -name "*-*-*.log" -mtime +7 -exec rm -f {} \; &>/dev/null &' >> /var/spool/cron/kkb
/bin/su - kkb -c 'python /home/kkb/videolocaldeploy/deploy_school.py >> /home/kkb/videolocaldeploy/log/$(date "+%Y-%m-%d").log 2>&1' &
/sbin/iptables -L | grep "tcp dpt:http" &> /dev/null
if [ $? -eq 0 ]
then
        echo "http firewall sucessful!"
else
	/sbin/iptables -I INPUT -p tcp --dport 80 -j ACCEPT
	echo "http firewall sucessful!"
fi
/sbin/iptables -L | grep "tcp dpt:https" &> /dev/null
if [ $? -eq 0 ]
then
        echo "https firewall sucessful!"
else
	/sbin/iptables -I INPUT -p tcp --dport 443 -j ACCEPT
	echo "https firewall sucessful!"
fi
/etc/init.d/iptables save &> /dev/null
/etc/init.d/iptables restart &> /dev/null
/usr/sbin/setenforce 0
ps aux| grep deploy_school | grep -v grep &> /dev/null
if [ $? -eq 0 ]
then
        echo "installed successfully!"
fi
