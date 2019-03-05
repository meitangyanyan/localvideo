#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
from log import logger_root


class URLMerge:

    urls = {'mp4': {}, 'gif': {}, 'srt': {}}

    def gen_data(self, fmt, prefix, uuid, suffix):
        # uuid格式：f1a9b386-868b-11e4-809c-5254005b49e4
        reg = r'^\w{8}\-(\w{4})\-(\w{4})\-\w{4}\-(\w{12})$'  # 分组UUID正则
        regex = re.compile(reg)
        rem = regex.match(uuid)
        # ret = {}

        if rem:
            remgps = rem.groups()
            dirstr = remgps[2] + '/' + remgps[1] + '/' + remgps[0]  # 获取UUID截断分组，并组合成存放路径
            if not self.urls[fmt].has_key(dirstr):  # 如当前格式中不含此路径，则添加
                self.urls[fmt].setdefault(dirstr, [])
            # 遍历文件名后缀，拼接成下载URL，并添加进该路径的列表中
            for suf in suffix:
                if fmt == 'gif':
                    self.urls[fmt][dirstr].append(prefix + suf + uuid + '.gif')
                else:
                    self.urls[fmt][dirstr].append(prefix + uuid + suf)

    def handle_err(self, errmsg):
        logger_root.error(errmsg)
        raise Exception, '%s' % errmsg

    def merge_from_url(self, fmt, prefix, uuids, suffix):
        if type(uuids) is list or type(uuids) is tuple:
            for uuid in uuids:
                self.gen_data(fmt, prefix, uuid, suffix)
        elif type(uuids) is str:
            self.gen_data(fmt, prefix, uuids, suffix)
        else:
            errmsg = 'uuids only accept list, tuple or str data type.'
            self.handle_err(errmsg)

    def url_merge(self, fmt, prefix, uuids):
        if not prefix.endswith('/'):
            prefix = prefix + '/'

        if fmt == 'mp4':
            suffix = (
                '_trans360p.mp4', '_trans480p.mp4', '_trans720p.mp4',)
            self.merge_from_url(fmt, prefix, uuids, suffix)
        elif fmt == 'gif':
            suffix = ('large_', 'middle_', 'normal_', 'small_', 'thumb_')
            self.merge_from_url(fmt, prefix, uuids, suffix)
        elif fmt == 'srt':
            suffix = ('.srt',)
            self.merge_from_url(fmt, prefix, uuids, suffix)
        else:
            errmsg = 'Incorrect file type:"%s"' % fmt
            self.handle_err(errmsg)
        return self.urls

    def get_url(self, data, mp4_prefix, gif_prefix, srt_prefix):
        mp4uuids = []
        gifuuids = []
        srtuuids = []

        if len(data):
            for i in range(len(data)):
                if data[i].has_key("filePath") and data[i]["filePath"] != '':
                    mp4uuids.append(data[i]["filePath"].split('.')[0].split('/')[4])
                if data[i].has_key("coverPath") and data[i]["coverPath"] != '':
                    gifuuids.append(data[i]["coverPath"].split('.')[0].split('/')[4])
                if data[i].has_key("srtPath") and data[i]["srtPath"] != '':
                    srtuuids.append(data[i]["srtPath"].split('.')[0].split('/')[4])
        self.url_merge('mp4', mp4_prefix, mp4uuids)
        self.url_merge('gif', gif_prefix, gifuuids)
        self.url_merge('srt', srt_prefix, srtuuids)
        # urls = mp4s + gifs + srts
        return self.urls



