import sys
import os
import mimetypes
import zipfile
import re

prog_name = ''

ws_out = 'bugreport_analysis'
ws_analysis = ws_out + '/' + 'analysis'
ws_analysis_build_details = ws_analysis + '/' + 'build_details.txt'
ws_analysis_sys_logs = ws_analysis + '/' + 'system_logs.txt'
ws_analysis_event_logs = ws_analysis + '/' + 'event_logs.txt'
ws_analysis_radio_logs = ws_analysis + '/' + 'radio_logs.txt'
ws_analysis_kernel_logs = ws_analysis + '/' + 'kernel_logs.txt'


ws_build_details = 'build_details.txt'
ws_report = 'report.txt'

# version
major_ver = '1'
minor_ver = '01'

mime_type_list = ['text/plain', 'application/zip']

# filename pattern
# bugreport-tphoneE-T5911INDURD-147-2018-04-25-11-45-07.txt


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


class WorkSpace(object):
    '''
    a class to store options to share accross
    global
    '''

    def __init__(self):
        self.file_version = None
        self.file_dumpstate_log = None
        self.file_main_entry = None
        self.dir_FS = None
        self.file_bugreport = None
        self.file_build_details = None
        self.file_system_logs = None
        self.file_event_logs = None
        self.file_radio_logs = None
        self.file_kernel_logs = None


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
