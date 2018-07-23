# import sys
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
file_ws_analysis_avc_logs       = dir_ws_analysis + '/' + 'avc_logs.txt'
file_ws_analysis_power_logs     = dir_ws_analysis + '/' + 'power_log.txt'



# events logs
dir_ws_analysis_events          = dir_ws_analysis + '/' + 'events'
file_ws_events_JP_data          = dir_ws_analysis_events + '/' + 'events_jp_data.txt'
file_ws_events_am_proc_start    = dir_ws_analysis_events + '/' + '01_events_am_proc_start.txt'
file_ws_events_am_proc_bound    = dir_ws_analysis_events + '/' + '02_events_am_proc_bound.txt'
file_ws_events_am_proc_died     = dir_ws_analysis_events + '/' + '03_events_am_proc_died.txt'

# system logs
file_ws_system_native_crash     = dir_ws_analysis + '/' + 'native_crashes.txt'
file_ws_system_app_crash        = dir_ws_analysis + '/' + 'app_crashes.txt'
file_ws_system_anr              = dir_ws_analysis + '/' + 'anr.txt'

# pid data
dir_ws_analysis_bypid           = dir_ws_analysis + '/' + 'byPid'

# report
file_ws_analysis_rpt            = dir_ws_analysis + '/' + 'report.txt'

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
        self.file_avc_logs = None
        self.file_ws_analysis_power_logs = None

        # events logs
        self.dir_ws_analysis_events = None
        self.file_ws_events_JP_data = None
        self.file_ws_events_am_proc_start = None
        self.file_ws_events_am_proc_bound = None
        self.file_ws_events_am_proc_died = None

        # system logs
        self.file_ws_system_native_crash = None
        self.file_ws_system_app_crash = None
        self.file_ws_system_anr = None
        # by pid data
        self.dir_ws_analysis_events_bypid = None

        # report
        self.file_analysis_rpt = None

class JavaProcess(object):
    """ 
     a class to hold java process info
    
     """
    def __init__(self):
        self.log_timestamp = None
        self.user = None
        self.pid = None
        self.uid = None
        self.name = None
        self.p_type= None
        self.component = None
        self.data_aps = None



OPT = Options()
WS = WorkSpace()
JP = JavaProcess()


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

# gen file open link for termial
def PrintTerminalLink(path):
    if not os.path.exists(WS.dir_out):
        return
    pathLink = 'file://' + os.path.abspath(path)
    PLOGV("link",pathLink)

def print_title(file_buf,title):
    file_buf.write(get_line())
    file_buf.write("--- " + title + "---")
    file_buf.write(get_empty_line())
    file_buf.write(get_line())
    file_buf.write(get_empty_line())