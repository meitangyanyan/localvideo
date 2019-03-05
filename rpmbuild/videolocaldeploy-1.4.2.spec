Name:           localvideodeploy
Version:	1.4.2        
Release:        1%{?dist}
Summary:        local video deploy

Group:          Applications/Internet
License:        GPL
URL:            http://www.cnblogs.com/meitangyanyan/
Source0:	tengine-1.5.2.tar.gz        
Source1:        nginx
Source2:	videolocaldeploy.tgz	
BuildRoot:	%_topdir/BUILDROOT

BuildRequires:  gcc gcc-c++ make
Requires:       python-setproctitle,openssl,openssl-devel,pcre-devel,pcre  

%description


%prep
%setup -c -n /root/rpmbuild/BUILD/ 


%build
cd /root/rpmbuild/BUILD/tengine-1.5.2
./configure  --user=kkb --group=kkb --prefix=/home/kkb/nginx --with-http_stub_status_module --with-http_ssl_module --with-http_gzip_static_module --with-http_concat_module
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd /root/rpmbuild/BUILD/tengine-1.5.2
make install DESTDIR=$RPM_BUILD_ROOT
%{__install} -p -D -m 0644 %{SOURCE1}/conf/* $RPM_BUILD_ROOT/home/kkb/nginx/conf/
%{__install} -p -D -m 0755 %{SOURCE1}/sbin/* $RPM_BUILD_ROOT/home/kkb/nginx/sbin/
%{__install} -p -D -m 0644 %{SOURCE1}/html/* $RPM_BUILD_ROOT/home/kkb/nginx/html/
%{__install} -p -D %{SOURCE2} $RPM_BUILD_ROOT/home/kkb/
mkdir $RPM_BUILD_ROOT/home/html/
%{__install} -p -D -m 0644 %{SOURCE1}/html/* $RPM_BUILD_ROOT/home/html/

%pre

id kkb &> /dev/null
if [ $? != 0 ];then
	/usr/sbin/useradd kkb 2> /dev/null
fi
%post
mkdir -p /home/kkb/nginx/{client_body,fastcgi,proxy,scgi,uwsgi}_temp &> /dev/null
/bin/tar zxf /home/kkb/videolocaldeploy.tgz -C /home/kkb &> /dev/null
/bin/rm -rf /home/kkb/videolocaldeploy.tgz
echo "/home/kkb/nginx/sbin/nginx &> /dev/null" >> /etc/rc.local
mkdir -p /home/html/lcms/video/{cover,file,srt} &> /dev/null
/bin/chown -R kkb:kkb  /home/html
/bin/chown -R kkb:kkb  /home/kkb/{nginx,videolocaldeploy}

%preun
ps aux| grep nginx | grep -v grep
if [ $? == 0 ];then
	/usr/bin/pkill -9 nginx > /dev/null 2>&1
fi
[ -d /home/kkb/nginx ] && /bin/rm -rf /home/kkb/nginx &> /dev/null
[ -d /home/kkb/videolocaldeploy ] && /bin/rm -rf /home/kkb/videolocaldeploy &> /dev/null

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,kkb,kkb,-)
/home/kkb
/home/html

%config
/home/kkb/nginx/conf/*

%changelog
