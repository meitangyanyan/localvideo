# localvideo

目录结构:
|---VideoLocalDeploy                  视频下载的源码目录
|---rpmbuild                          rpm包打包目录:生成本地视频部署rpm包
|---epel-release-6-8.noarch.rpm
|---RPM-GPG-KEY-GXB
|---local_video_course_deploy.sh      本地视频部署一键部署脚本(课程id版)
|---local_video_school_deploy.sh      本地视频部署一键部署脚本(学校id版)
|---ssl.py                            自签名证书生成脚本

使用说明:
VideoLocalDeploy 为视频下载的源码目录,功能是下载课程视频,可直接配合nginx实现本地视频服务器
rpmbuild 将VideoLocalDeploy和nginx打成一个rpm包,安装rpm包可搭建本地视频服务器
