import sys
import os
import getopt
import mimetypes
import zipfile
import shutil
import glob
import re
import time

import buganalysis_utils as util
import buganalysis_config as config
import buganalysis_pattern as patt
import buganalysis_dump as dump


import buganalysis_analyzer as analyzer
from reports import report as rpt

start_time = time.time()
'''
This is tool to get bugreport analysis

TODO:
1. Open bugreport from cmdline
    - check , Is it zip or .txt
    - Extract if it is zip and open .txt
2. Get build details for .txt file
3. Display build details and device information
4. Prepare CLI to shor the data as per user request
5. Add CLI option to short data with default configuration

Structure:

bugreport_analysis/
|-- build_details.txt
`-- report.txt


command:
    bugreport_analysis.py -v --file bugreport.zip

'''

# ------------------------
# this
# -----------------------

# get options object and all config
OPT = util.OPT
WS = util.WS


debug_enable = config.MODE_DEBUG
test_enable = config.MODE_TEST

TAG = os.path.basename(__file__)


def setup_ws():
    WS.dir_out              = OPT.out
    WS.dir_ws               = OPT.out + '/' + util.dir_ws
    WS.dir_ws_analysis      = OPT.out + '/' + util.dir_ws_analysis
    WS.file_build_details   = OPT.out + '/' + util.file_ws_analysis_build_details
    WS.file_kernel_logs     = OPT.out + '/' + util.file_ws_analysis_kernel_logs
    WS.file_system_logs     = OPT.out + '/' + util.file_ws_analysis_sys_logs
    WS.file_event_logs      = OPT.out + '/' + util.file_ws_analysis_event_logs
    WS.file_radio_logs      = OPT.out + '/' + util.file_ws_analysis_radio_logs
    WS.file_sys_prop        = OPT.out + '/' + util.file_ws_analysis_sys_prop
    WS.file_devinfo         = OPT.out + '/' + util.file_ws_analysis_devinfo
    WS.file_avc_logs        = OPT.out + '/' + util.file_ws_analysis_avc_logs
    WS.file_ws_analysis_power_logs = OPT.out + '/' + util.file_ws_analysis_power_logs

    # events logs
    WS.dir_ws_analysis_events           = OPT.out + '/' + util.dir_ws_analysis_events
    WS.file_ws_events_JP_data           = OPT.out + '/' + util.file_ws_events_JP_data
    WS.file_ws_events_am_proc_start     = OPT.out + '/' + util.file_ws_events_am_proc_start
    WS.file_ws_events_am_proc_bound     = OPT.out + '/' + util.file_ws_events_am_proc_bound
    WS.file_ws_events_am_proc_died      = OPT.out + '/' + util.file_ws_events_am_proc_died

    # system logs
    WS.file_ws_system_native_crash      = OPT.out + '/' + util.file_ws_system_native_crash
    WS.file_ws_system_app_crash         = OPT.out + '/' + util.file_ws_system_app_crash
    WS.file_ws_system_anr               = OPT.out + '/' + util.file_ws_system_anr

    # By pid data
    WS.dir_ws_analysis_bypid            = OPT.out + '/' + util.dir_ws_analysis_bypid

    # report
    WS.file_analysis_rpt                = OPT.out + '/' + util.file_ws_analysis_rpt


    try:
        if os.path.exists(WS.dir_out):
            shutil.rmtree(WS.dir_out)
        os.makedirs(WS.dir_out)
        os.makedirs(WS.dir_ws)
        os.makedirs(WS.dir_ws_analysis)
        os.makedirs(WS.dir_ws_analysis_events)
        os.makedirs(WS.dir_ws_analysis_bypid)

    except os.error as err:
        util.PLOGE(TAG, str(err), exit=False)
        return False
    return True


def prepare_bugreport_raw_data():
    if not setup_ws():
        util.PLOGE(TAG, 'failed to setup ws', exit=False)
        return False

    is_unzip_required, error = util.is_unzip_required(OPT.zip_file)

    if error:
        util.PLOGE(
            TAG, 'bugreport file type wrong, expected TEXT or ZIP ', exit=False)
        return False

    if is_unzip_required:
        util.PLOGV(TAG, 'Extracting ... : ' + OPT.file_name)
        with zipfile.ZipFile(OPT.zip_file, 'r') as bug_zip:
            try:
                bug_zip.extractall(WS.dir_ws)
            except zipfile.BadZipfile:
                util.PLOGE(TAG, 'Badzipfile', exit=False)
                return False
            except zipfile.LargeZipFile:
                util.PLOGE(TAG, 'LargeZipFile', exit=False)
                return False
    return True


def check_prerequisite():

    if not OPT.file_name:
        util.PLOGE(TAG,'bug report file not given in termial command line ')
        return False

    if not OPT.out:
        util.PLOGE(TAG,'out dir not givent in terminal command line')
        return False

    patt_out = re.compile(r'^[.]')
    if patt_out.search(OPT.out):
        util.PLOGE(TAG,'out dir is a current or previous dir. please give name for dir')
        return False

    file_path = os.path.dirname(os.path.realpath(OPT.file_name))
    util.PLOGV(TAG," file : " + file_path )
    util.PLOGV(TAG," out  : " + os.path.realpath(OPT.out))

    if file_path == os.path.realpath(OPT.out):
        util.PLOGE(TAG,'out dir and file is in same dir. please give different dir')
        return False


    OPT.zip_file = os.path.abspath(OPT.file_name)
    if not os.path.isfile(OPT.zip_file):
        util.PLOGE(TAG, 'File not found or is not a file : ',
                   OPT.zip_file, exit=False)
        return False

    is_unzip_required, error = util.is_unzip_required(OPT.zip_file)

    if error:
        util.PLOGE(
            TAG, 'bugreport file type wrong, expected TEXT or ZIP ', exit=False)
        return False
    else:
        util.PLOGV(TAG,'bugreport zip file found : ' + str(is_unzip_required))

    return True


def set_files_path():
    files_list = glob.glob(WS.dir_ws + '/*')
    util.PLOGV(TAG, 'Files in side zip')
    util.PLOGV(TAG, files_list)

    for file_and_folder in files_list:
        if patt.pattern_version_file_wt_txt_ext.search(file_and_folder):
            WS.file_version = file_and_folder
        elif patt.pattern_dumpstate_log_file_wt_txt_ext.search(file_and_folder):
            WS.file_dumpstate_log = file_and_folder
        elif patt.pattern_main_entry_file_wt_txt_ext.search(file_and_folder):
            WS.file_main_entry = file_and_folder
        elif patt.pattern_FS_dir.search(file_and_folder):
            WS.dir_FS = file_and_folder
        elif patt.pattern_bug_rpt_file_wt_txt_ext.search(file_and_folder):
            WS.file_bugreport = file_and_folder

    util.PLOGV(TAG, WS.file_version)
    util.PLOGV(TAG, WS.file_dumpstate_log)
    util.PLOGV(TAG, WS.file_main_entry)
    util.PLOGV(TAG, WS.dir_FS)
    util.PLOGV(TAG, WS.file_bugreport)

    util.PLOGV(TAG,WS.file_build_details)
    util.PLOGV(TAG,WS.file_kernel_logs)
    util.PLOGV(TAG,WS.file_system_logs)
    util.PLOGV(TAG,WS.file_event_logs)
    util.PLOGV(TAG,WS.file_radio_logs)
    util.PLOGV(TAG,WS.file_sys_prop)
    util.PLOGV(TAG,WS.file_avc_logs)
    util.PLOGV(TAG,WS.file_ws_analysis_power_logs)

    util.PLOGV(TAG,WS.file_analysis_rpt)
    util.PLOGV(TAG,WS.file_ws_system_native_crash)
    util.PLOGV(TAG,WS.file_ws_system_app_crash)
    util.PLOGV(TAG,WS.file_ws_system_anr)

    if not WS.file_bugreport:
        return False
    return True

def DumpAnalysisPaths():
    util.PLOGV(TAG,util.get_line())
    util.PrintTerminalLink(WS.dir_out)
    util.PrintTerminalLink(WS.dir_ws)
    util.PrintTerminalLink(WS.dir_ws_analysis)
    util.PrintTerminalLink(WS.file_build_details)
    util.PrintTerminalLink(WS.file_kernel_logs)
    util.PrintTerminalLink(WS.file_system_logs)
    util.PrintTerminalLink(WS.file_event_logs)
    util.PrintTerminalLink(WS.file_radio_logs)
    util.PrintTerminalLink(WS.file_sys_prop)
    util.PrintTerminalLink(WS.file_devinfo)
    util.PrintTerminalLink(WS.file_avc_logs)
    util.PrintTerminalLink(WS.file_ws_analysis_power_logs)
    util.PrintTerminalLink(WS.dir_ws_analysis_events)
    util.PrintTerminalLink(WS.file_ws_events_JP_data)
    util.PrintTerminalLink(WS.file_ws_events_am_proc_start)
    util.PrintTerminalLink(WS.file_ws_events_am_proc_bound)
    util.PrintTerminalLink(WS.file_ws_events_am_proc_died)
    util.PrintTerminalLink(WS.file_ws_system_native_crash)
    util.PrintTerminalLink(WS.file_ws_system_app_crash)
    util.PrintTerminalLink(WS.file_ws_system_anr)
    util.PrintTerminalLink(WS.dir_ws_analysis_bypid)
    util.PrintTerminalLink(WS.file_analysis_rpt)

    # report
    util.PLOGV(TAG,util.get_line())

def analyze_bugreport():
    # Get build details
    util.PLOGV(TAG, 'Enter  - analyze_bugreport')
    dump.extract_data_files(WS)
    dump.avc_logs(WS)
    analyzer.StartEventAnaylzer(WS)
    analyzer.StartSystemAnaylzer(WS)
    DumpAnalysisPaths()
    util.PLOGV(TAG, 'Exit   - analyze_bugreport')
    return True
# Generate report
# Bug ID        :
# Bug title     :
# Dev Enginner  :
# Test Enginner :
# Build details :
# Device details:
# Device onwer  :
# Device account:
#
# Root cause :
# Uptime     :
# Storage    :
# Network    :


def GenReport():
    if not rpt.GenReport(WS):
        util.PLOGE(TAG,'failed to get report', exit=True)

def start_analysis():
    # check cmd line args
    if not check_prerequisite():
        usage()
        util.PLOGE(TAG, 'check prerequitsite failed', exit=True)
    if not prepare_bugreport_raw_data():
        util.PLOGE(TAG, 'Prepare bugreport data failed', exit=True)
    if not set_files_path():
        util.PLOGE(TAG, 'failed to set file path', exit=True)
    if not analyze_bugreport():
        util.PLOGE(TAG, 'Failed to analyze bugreport', exit=True)


def usage():
    util.print_empty_line()
    print util.prog_name + ' ' + '<options> ' + ' --file ' + ' bugreport.zip '
    util.print_line()
    print 'options:'
    print '\t-h,--help\t\t - print help'
    print '\t-v,--verbose\t\t - print verbose logging'
    print '\t--file <filename>\t - zip or txt file of bugreport'
    print '\t--out <out_dir>\t\t - output dir'
    print '\t--bugnum <bug number>\t\t - Redmine bug number'
    print '\t--version\t\t - print version'
    util.print_empty_line()


def parse_argument(argv):
    long_opts = ['help', 'version', 'verbose', 'file=', 'out=', 'bugnum=']
    short_opts = 'hvl'

    try:
        opts_list, args_pos = getopt.getopt(argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        util.print_empty_line()
        print 'Error : args parser '
        usage()
        return False

    util.PLOGV(TAG, 'opts are :', str(opts_list))
    util.PLOGV(TAG, 'args are :', str(args_pos))

    if args_pos:
        usage()
        return False

    for opt, val in opts_list:
        if opt == '--file':
            util.OPT.file_name = val
        elif opt == '--out':
            util.OPT.out = val
        elif opt == '--bugnum':
            util.OPT.bug_num = val
        elif opt in ['-h', '--help']:
            usage()
            return False
        elif opt == '--version':
            print util.get_version()
            return False
        elif opt in ['-v', '--verbose']:
            util.OPT.verbose = True
        else:
            print 'Error: wrong option : ' + opt
            return False

    return True

def main():
    util.prog_name = sys.argv[0]
    if not parse_argument(sys.argv):
        util.PLOGE(TAG, 'parse argument failed', exit=True)
    start_analysis()
    GenReport()
    time_str = "--- %s seconds ---" % (time.time() - start_time)
    util.PLOGD(TAG,time_str)


if __name__ == '__main__':
    main()
