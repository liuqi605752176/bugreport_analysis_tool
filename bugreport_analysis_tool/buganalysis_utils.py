import sys
import os
import mimetypes
import zipfile
import re

prog_name = ''

dir_ws                          = 'bugreport_analysis'
dir_ws_analysis                 = dir_ws + '/' + 'analysis'
file_ws_analysis_build_details  = dir_ws_analysis + '/' + 'build_details.txt'
file_ws_analysis_sys_logs       = dir_ws_analysis + '/' + 'system_logs.txt'
file_ws_analysis_event_logs     = dir_ws_analysis + '/' + 'event_logs.txt'
file_ws_analysis_radio_logs     = dir_ws_analysis + '/' + 'radio_logs.txt'
file_ws_analysis_kernel_logs    = dir_ws_analysis + '/' + 'kernel_logs.txt'
file_ws_analysis_sys_prop       = dir_ws_analysis + '/' + 'system_prop.txt'
file_ws_analysis_devinfo        = dir_ws_analysis + '/' + 'devinfo.txt'

# version
major_ver = '1'
minor_ver = '01'
mime_type_list = ['text/plain', 'application/zip']

class Options(object):
    '''
    a class to store options to share accross
    global
    '''

    def __init__(self):
        self.file_name = None
        self.verbose = None
        self.is_unzip_required = None
        self.zip_file = None
        self.out = None


class WorkSpace(object):
    '''
    a class to store options to share accross
    global
    '''

    def __init__(self):
        self.dir_out = None
        self.dir_ws = None
        self.dir_ws_analysis = None

        self.file_version = None
        self.file_dumpstate_log = None
        self.file_main_entry = None
        self.dir_FS = None
        self.file_bugreport = None
        self.file_build_details = None
        self.file_kernel_logs = None
        self.file_system_logs = None
        self.file_event_logs = None
        self.file_radio_logs = None
        self.file_sys_prop = None
        self.file_devinfo = None



OPT = Options()
WS = WorkSpace()



def get_line(symbol='-', len=90):
    line = symbol * len
    return line + '\n'

def get_empty_line():
    line = '' + '\n'
    return line

def print_line(symbol='-', len=90):
    print symbol * len

def print_empty_line():
    print ''


def get_version():
    version = 'Bugreport anaysis' + '- V' + major_ver + '.' + minor_ver
    return version


def get_log_msg(tag, log_type, msg, arg=None):
    if type(msg) != str:
        log_msg = tag + ' ' + log_type + ':  ' + str(msg) + ' ' + arg
    else:
        log_msg = tag + ' ' + log_type + ':  ' + msg + ' ' + arg
    return log_msg


def PLOGE(tag='tag', msg=None, arg='None', exit=False):
    log_type = 'E'
    log_msg = get_log_msg(tag, log_type, msg, arg)
    print log_msg
    if exit is True:
        os.sys.exit(-1)


def PLOGD(tag='', msg='', arg=''):
    log_type = 'D'
    log_msg = get_log_msg(tag, log_type, msg, arg)
    print log_msg


def PLOGV(tag='', msg='', arg=''):
    if OPT.verbose:
        log_type = 'V'
        log_msg = get_log_msg(tag, log_type, msg, arg)
        print log_msg


def is_unzip_required(file_path):
    mime_type = mimetypes.guess_type(file_path)

    if mime_type[0] not in mime_type_list:
        return False, True

    if mime_type[0] == 'application/zip':
        if not zipfile.is_zipfile(file_path):
            return False, True
        return True, False
    else:
        return False, False
