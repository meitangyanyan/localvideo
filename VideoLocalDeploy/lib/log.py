#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, string
import logging
import logging.config

# Color escape string
COLOR_RED = '\033[1;31m'
COLOR_GREEN = '\033[1;32m'
COLOR_YELLOW = '\033[1;33m'
COLOR_BLUE = '\033[1;34m'
COLOR_PURPLE = '\033[1;35m'
COLOR_CYAN = '\033[1;36m'
COLOR_GRAY = '\033[1;37m'
COLOR_WHITE = '\033[1;38m'
COLOR_RESET = '\033[1;0m'

LOG_COLORS = {
    'DEBUG': '%s',
    'INFO': COLOR_GREEN + '%s' + COLOR_RESET,
    'WARNING': COLOR_YELLOW + '%s' + COLOR_RESET,
    'ERROR': COLOR_RED + '%s' + COLOR_RESET,
    'CRITICAL': COLOR_RED + '%s' + COLOR_RESET,
    'EXCEPTION': COLOR_PURPLE + '%s' + COLOR_RESET,
}


class ColorFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        level_name = record.levelname
        msg = logging.Formatter.format(self, record)

        return LOG_COLORS.get(level_name, '%s') % msg


def _create_formatters(cp):
    flist = cp.get("formatters", "keys")
    if not len(flist):
        return {}
    flist = string.split(flist, ",")
    flist = logging.config._strip_spaces(flist)
    formatters = {}
    for form in flist:
        sectname = "formatter_%s" % form
        opts = cp.options(sectname)
        if "format" in opts:
            fs = cp.get(sectname, "format", 1)
        else:
            fs = None
        if "datefmt" in opts:
            dfs = cp.get(sectname, "datefmt", 1)
        else:
            dfs = None
        c = ColorFormatter
        if "class" in opts:
            class_name = cp.get(sectname, "class")
            if class_name:
                c = logging.config._resolve(class_name)
        f = c(fs, dfs)
        formatters[form] = f
    return formatters


def fileConfig(fname, defaults=None, disable_existing_loggers=1):
    import ConfigParser

    cp = ConfigParser.ConfigParser(defaults)
    if hasattr(cp, 'readfp') and hasattr(fname, 'readline'):
        cp.readfp(fname)
    else:
        cp.read(fname)
    formatters = _create_formatters(cp)
    logging._acquireLock()
    try:
        logging._handlers.clear()
        del logging._handlerList[:]
        handlers = logging.config._install_handlers(cp, formatters)
        logging.config._install_loggers(cp, handlers, disable_existing_loggers)
    finally:
        logging._releaseLock()

# cur_dir = os.path.split(os.path.realpath(__file__))[0]
# if not os.path.exists(cur_dir + '/../log/localdeploy.log'):
# f = file(cur_dir + '/../log/localdeploy.log', 'w')
#     f.close()


fileConfig('%s/../conf/logging.conf' % os.path.split(os.path.realpath(__file__))[0])
logger_rotatefile = logging.getLogger('rotatefile')
logger_console = logging.getLogger('console')
logger_root = logging.getLogger('root')