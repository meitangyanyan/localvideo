#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib2
import commands
from Queue import Queue
from lib.ParseConfig import Config
from lib.log import logger_root
from lib.UrlMerge import URLMerge
from lib.mailtome import send_mail


# 本地部署API调用URL，需根据实际URL配置
api_get_prefix = 'http://xxx/videos/course'  # 下载列表API前缀

# 调用Config类，解析配置文件中的配置
config = Config()
course_id_list = config.get_course_id().split("|")  # 课程ID列表
prefixs = config.get_prefixs()  # mp4,gif,srt下载连接前缀，目前是七牛空间的
dirs = config.get_dirs()  # mp4,gif,srt各类文件下载后存放路径
api_get_url_list = []
for course_id in course_id_list:
    api_get_url_list.append(api_get_prefix + '/' + course_id + '/api')  # 当前课程的下载列表API链接

def init_queue(url_dicts):
    queue = Queue()
    for fk in url_dicts.keys():
        for dk in url_dicts[fk].keys():
            dir = dirs[fk + '_dir'] + '/' + dk + '/'  # 实际文件存放路径
            if not os.path.exists(dir):
                os.makedirs(dir)
            for url in url_dicts[fk][dk]:
                queue.put((dir, url))  # 生成下载队列
    return queue

def http_get(api_get_url):
    response = urllib2.urlopen(api_get_url)         #调用urllib2向服务器发送get请求
    return response.read()


if __name__ == '__main__':
    cur_pid = os.getpid()
    s, o = commands.getstatusoutput("ps aux | grep 'kaikeba videolocaldeploy' | grep -Ev '(grep|%s)'" % cur_pid)
    if s:
        #URL合并类
        urlmerge = URLMerge()
        i=1
        #调用api获得下载视频的
        for api_get_url in api_get_url_list:
            rest = http_get(api_get_url)
            url_dic=eval(rest)

            if url_dic['code'] == 200:
                logger_root.info('api调用成功!')
                if url_dic.has_key("data") and len(url_dic["data"]):
                    logger_root.info('第%d个课程id下有视频！' % i)
                    urldicts = urlmerge.get_url(url_dic["data"], mp4_prefix=prefixs['mp4_prefix'], gif_prefix=prefixs['gif_prefix'],
                                                srt_prefix=prefixs['srt_prefix'])  #生成下载信息dict

                    q = init_queue(urldicts)  #初始化下载队列
                    while True:
                        output = commands.getoutput('ps aux|grep wget|grep -v grep|wc -l')
                        if q.empty():
                            logger_root.info('第%d个课程下的所有视频都下载完成!' % i)
                            if i == len(api_get_url_list):
                                send_mail("本地部署course%s" % course_id_list,"所有视频都下载完成!")
                            break
                        elif int(output) <= 10:
                            aa=q.get()
                            download_dir=aa[0]
                            download_url=aa[1]
                            fname = download_dir + os.path.basename(download_url)
                            if not os.path.exists(download_dir):
                                os.system('mkdir %s' % download_dir)
                            logger_root.info('正在下载%s....' % fname)
                            os.system('wget -b -q -N -c -P %s %s' % (download_dir,download_url))
                else:
                    logger_root.error('无法获得下载视频的uuid，原因是第%d个课程id下没有视频！' % i)
                    send_mail("本地部署course%s" % course_id_list,"无法获得下载视频的uuid，原因是第%d个课程id下没有视频！" % i)
            else:
                logger_root.error('无法获得下载视频的uuid，原因是是api调用不成功！')
                send_mail("本地部署course%s" % course_id_list,"无法获得下载视频的uuid，原因是是api调用不成功！")
            i+=1
    else:
        logger_root.error('There is a same progress is running!')

