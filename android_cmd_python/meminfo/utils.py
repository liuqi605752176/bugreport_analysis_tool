import sys
import os
import mimetypes
import zipfile

prog_name = ''
ws_out = 'bugreport_analysis'
ws_build_details = 'build_details.txt'
ws_report = 'report.txt'

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
        self.verbose = None
        self.meminfo = None
        self.ion = None
        self.ionAndMeminfo = None


class WorkSpace(object):
    '''
    a class to store options to share accross 
    global 
    '''

    def __init__(self):
        self.bugreport_filename = None


OPT = Options()
WS = WorkSpace()


def print_line(symbol='-', len=90):
    print symbol * len


def print_empty_line():
    print ''


def get_version():
    version = 'Bugreport anaysis' + '- V' + major_ver + '.' + minor_ver
    return version


def get_log_msg(tag, log_type, msg, arg=None):
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
