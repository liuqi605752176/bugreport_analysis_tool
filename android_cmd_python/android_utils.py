# import sys
import os
import mimetypes
import zipfile
import re

prog_name = ''


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
        self.debug = None
        self.pid = None



OPT = Options()



def clean_me(filename):
    if not os.path.isfile(filename):
        PLOGE('Error','file not found : ' + str(filename))
        return False
    os.remove(filename)
    return True

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
    tag = tag  + ' ' * (25 - len(tag))
    if type(msg) != str:
        log_msg = tag + ' ' + log_type + ':  ' + str(msg) + ' ' + arg
    else:
        log_msg = tag + ' ' + log_type + ':  ' + msg + ' ' + arg
    return log_msg


def PLOGE(tag='tag', msg=None, arg='None', exit=False ,strip=False):
    log_type = 'E'
    log_msg = get_log_msg(tag, log_type, msg, arg)
    if not strip:
        print log_msg
    else:
        print log_msg,
    if exit is True:
        os.sys.exit(-1)


def PLOGD(tag='', msg='', arg='',strip=False):
    if OPT.debug:
        log_type = 'D'
        log_msg = get_log_msg(tag, log_type, msg, arg)
        if not strip:
            print log_msg
        else:
            print log_msg,

def PLOGV(tag='', msg='', arg='',strip=False):
    if OPT.verbose:
        log_type = 'V'
        log_msg = get_log_msg(tag, log_type, msg, arg)
        if not strip:
            print log_msg
        else:
            print log_msg,


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

def dump_data_to_screen(tag,buf):
    if type(list):
      for item in buf:
         PLOGD(tag,item)
    elif type(file):
        if os.path.isfile(str(buf)):
            with open(buf,'rU') as f_buf:
                for line in f_buf:
                    PLOGD(tag,line,strip=True)
            f_buf.close()
    elif type(buf) == str:
        PLOGD(tag,buf,strip=True)
    else:
        PLOGD(tag,str(buf),strip=True)
