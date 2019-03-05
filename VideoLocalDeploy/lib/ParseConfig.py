#! /usr/bin/env python
# -*- coding: utf-8 -*

import os
from ConfigParser import ConfigParser
from lib.log import logger_root

cf = ConfigParser()


class Config:
    school_id = ''
    course_id = ''
    mp4_dir = gif_dir = srt_dir = ''
    mp4_prefix = gif_prefix = srt_prefix = ''
    ret = ''
    errmsg = ''

    def __init__(self):
        cf.read('%s/../conf/setting.conf' % os.path.split(os.path.realpath(__file__))[0])
        Config.school_id = cf.get('main', 'school_id')
        Config.course_id = cf.get('main', 'course_id')
        Config.mp4_dir = cf.get('storage', 'mp4_dir')
        Config.gif_dir = cf.get('storage', 'gif_dir')
        Config.srt_dir = cf.get('storage', 'srt_dir')
        Config.mp4_prefix = cf.get('download', 'mp4_prefix')
        Config.gif_prefix = cf.get('download', 'gif_prefix')
        Config.srt_prefix = cf.get('download', 'srt_prefix')

    def get_school_id(self):
        if Config.school_id != '':
            self.ret = Config.school_id
        else:
            self.errmsg = 'school_id config was None.'
            logger_root.error(self.errmsg)
            raise Exception, '%s' % self.errmsg
        return self.ret

    def get_course_id(self):
        if Config.course_id != '':
            self.ret = Config.course_id
        else:
            self.errmsg = 'course_id config was None.'
            logger_root.error(self.errmsg)
            raise Exception, '%s' % self.errmsg
        return self.ret

    def get_dirs(self):
        dirs = {}
        if Config.mp4_dir == '':
            self.errmsg = 'mp4_dir config was None.'
            logger_root.warning(self.errmsg)
            self.ret = Config.mp4_dir = '/home/kkb/nginx/html/lcms/video/file'

        if Config.gif_dir == '':
            self.errmsg = 'gif_dir config was None.'
            logger_root.warning(self.errmsg)
            self.ret = Config.gif_dir = '/home/kkb/nginx/html/lcms/video/cover'

        if Config.srt_dir == '':
            self.errmsg = 'srt_dir config was None.'
            logger_root.warning(self.errmsg)
            self.ret = Config.srt_dir = '/home/kkb/nginx/html/lcms/video/srt'

        dirs = {'mp4_dir': Config.mp4_dir, 'gif_dir': Config.gif_dir,
                'srt_dir': Config.srt_dir}
        for dir in dirs.values():
            self.__make_dir(dir)
        self.ret = dirs
        return self.ret

    def get_prefixs(self):
        prefixs = {}
        if Config.mp4_prefix != '':
            prefixs['mp4_prefix'] = Config.mp4_prefix
        else:
            self.errmsg = 'mp4_prefix config was None.'
            logger_root.error(self.errmsg)
            raise Exception, '%s' % self.errmsg

        if Config.gif_prefix != '':
            prefixs['gif_prefix'] = Config.gif_prefix
        else:
            self.errmsg = 'gif_prefix config was None.'
            logger_root.error(self.errmsg)
            raise Exception, '%s' % self.errmsg

        if Config.srt_prefix != '':
            prefixs['srt_prefix'] = Config.srt_prefix
        else:
            self.errmsg = 'srt_prefix config was None.'
            logger_root.error(self.errmsg)
            raise Exception, '%s' % self.errmsg

        self.ret = prefixs
        return self.ret

    def __make_dir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)