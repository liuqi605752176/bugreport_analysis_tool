import sys
import os
import getopt
import mimetypes
import zipfile
import shutil
import glob
import re

import utils as util
import config
import logPattern as patt

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

TAG = 'bugreport_analysis'


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
    try:
        if os.path.exists(WS.dir_out):
            shutil.rmtree(WS.dir_out)
        os.makedirs(WS.dir_out)
        os.makedirs(WS.dir_ws)
        os.makedirs(WS.dir_ws_analysis)
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
    if not WS.file_bugreport:
        return False
    return True


def analyze_bugreport():
    # Get build details
    util.PLOGV(TAG, 'Enter  - analyze_bugreport')

    def dump_build_details(file_buf):
        try:
            f_build_details = open(WS.file_build_details,'w+')
        except IOError as err:
            err_str = 'failed to create file : ' + \
                WS.file_build_details + '\n' + str(err)
            util.PLOGE(TAG, err_str)
            return False

        f_build_details.write(util.get_line())
        f_build_details.write('--- Build details ---\n')
        f_build_details.write(util.get_line())

        for line in file_buf:
            if patt.start_of_file.match(line):
                continue
            if patt.start_dumpsys_meminfo.search(line):
                break
            f_build_details.write(line)

        f_build_details.write(util.get_empty_line())
        f_build_details.close()
        return True

    ## TODO: optimise in single function
    def dump_kernel_logs(file_buf):
        bool_start_dump = False
        try:
            f_kernel_logs = open(WS.file_kernel_logs,'w+')
        except IOError as err:
            err_str = 'failed to create file : ' + WS.file_kernel_logs + \
                '\n' + str(err)
            util.PLOGE(TAG,err_str)
            return False

        f_kernel_logs.write(util.get_line())
        f_kernel_logs.write('--- Kernel logs (dmesg) ---\n')
        f_kernel_logs.write(util.get_line())

        for line in file_buf:
            # print line,
            if bool_start_dump:
                f_kernel_logs.write(line)
            if patt.start_kernel_log.search(line):
                bool_start_dump = True
            if patt.end_kernel_log.search(line):
                bool_start_dump = False
                break

        f_kernel_logs.write(util.get_empty_line())
        f_kernel_logs.close()
        return True

    ## TODO: optimise in single function
    def dump_system_logs(file_buf):
        bool_start_dump = False
        try:
            f_sys_log_buf = open(WS.file_system_logs,'w+')
        except IOError as err:
            err_str = 'failed to create file : ' \
                + WS.file_system_logs + '\n' + str(err)
            util.PLOGE(TAG,err_str)
            return False
        f_sys_log_buf.write(util.get_line())
        f_sys_log_buf.write('--- System logs ---\n')
        f_sys_log_buf.write(util.get_line())

        for line in file_buf:
            if bool_start_dump:
                f_sys_log_buf.write(line)
            if patt.start_system_log.search(line):
                bool_start_dump = True
            if patt.end_system_log.search(line):
                bool_start_dump = False
                break
            # if bool_start_dump:
            #     f_sys_log_buf.write(line)

        f_sys_log_buf.write(util.get_line())
        f_sys_log_buf.close()
        return True

    ## TODO: optimise in single function
    def dump_event_logs(file_buf):
        bool_start_dump = False
        try:
            f_event_logs = open(WS.file_event_logs,'w+')
        except IOError as err:
            err_str = 'failed to create file : ' + WS.file_event_logs + \
                '\n' + str(err)
            util.PLOGE(TAG,err_str)
            return False

        f_event_logs.write(util.get_line())
        f_event_logs.write('--- Events logs ---\n')
        f_event_logs.write(util.get_line())

        for line in file_buf:
            if bool_start_dump:
                f_event_logs.write(line)
            if patt.start_event_log.search(line):
                bool_start_dump = True
            if patt.end_event_log.search(line):
                bool_start_dump = False
                break

        f_event_logs.write(util.get_empty_line())
        f_event_logs.close()
        return True

    ## TODO: optimise in single function
    def dump_radio_logs(file_buf):
        bool_start_dump = False
        try:
            f_radio_logs = open(WS.file_radio_logs,'w+')
        except IOError as err:
            err_str = 'failed to create file : ' + WS.file_radio_logs + \
                '\n' + str(err)
            util.PLOGE(TAG,err_str)
            return False

        f_radio_logs.write(util.get_line())
        f_radio_logs.write('--- Radio logs ---\n')
        f_radio_logs.write(util.get_line())

        for line in file_buf:
            if bool_start_dump:
                f_radio_logs.write(line)
            if patt.start_radio_log.search(line):
                bool_start_dump = True
            if patt.end_radio_log.search(line):
                bool_start_dump = False
                break

        f_radio_logs.write(util.get_empty_line())
        f_radio_logs.close()
        return True

    def dump_sys_prop(file_buf):

        def get_prop_val(prop):
            list_prop_val = str(prop).split(': [')
           # print list_prop_val
            return list_prop_val[1].strip('\n').strip(']')

        bool_start_dump = False

        try:
            f_sys_prop = open(WS.file_sys_prop, 'w+')
        except IOError as err:
            err_str = 'failed to create file : ' + Ws.file_sys_prop + \
                str(err)
            util.PLOGE(TAG,err_str)
            return False

        f_sys_prop.write(util.get_line())
        f_sys_prop.write('--- system properties ---\n')
        f_sys_prop.write(util.get_line())

        for line in file_buf:
            if bool_start_dump:
                f_sys_prop.write(line)

            if patt.start_sys_properties.search(line):
                bool_start_dump = True

            if patt.end_sys_properties.search(line):
                bool_start_dump = False
                break

        f_sys_prop.write(util.get_empty_line())
        f_sys_prop.close()

        # dump device info at runtime

        try:
            f_sys_prop = open(WS.file_sys_prop, 'r')
        except IOError as err:
            err_str  = 'failed to read file : ' + WS.file_sys_prop + str(err)
            util.PLOGE(TAG,err_str)
            return False

        device_product_name = ''
        device_factory_serial_num = ''
        device_hw_serial_num = ''
        device_build_id = ''
        device_build_fingerprint = ''
        device_build_date = ''
        device_kernel_build_date = ''
        device_kernel_build_user = ''
        device_mpss_baseband1_build = ''
        device_mpss_baseband_build = ''
        device_gms_build = ''
        device_kernel_build_user = ''
        device_security_patch_level = ''
        device_slot_suffix = ''

        for line in f_sys_prop:
            if patt.device_product_name.search(line):
                device_product_name = 'Device product name                 : ' + get_prop_val(line)
            elif patt.device_factory_serial_num.search(line):
                device_factory_serial_num = 'Device factory serial number        : ' + get_prop_val(line)
            elif patt.device_hw_serial_num.search(line):
                device_hw_serial_num = 'Device hardware serial number name  : ' + get_prop_val(line)
            elif patt.device_build_id.search(line):
                device_build_id = 'Device build id                     : ' + get_prop_val(line)
            elif patt.device_build_fingerprint.search(line):
                device_build_fingerprint = 'Device build fingerprint            : ' + get_prop_val(line)
            elif patt.device_build_date.search(line):
                device_build_date = 'Device build date                   : ' + get_prop_val(line)
            elif patt.device_kernel_build_date.search(line):
                device_kernel_build_date = 'Device kernel build date            : ' + get_prop_val(line)
            elif patt.device_kernel_build_user.search(line):
                device_kernel_build_user = 'Device kernel build user            : ' + get_prop_val(line)
            elif patt.device_mpss_baseband1_build.search(line):
                device_mpss_baseband1_build = 'Device mpss baseband1 build         : ' + get_prop_val(line)
            elif patt.device_mpss_baseband_build.search(line):
                device_mpss_baseband_build = 'Device mpss baseband build          : ' + get_prop_val(line)
            elif patt.device_gms_build.search(line):
                device_gms_build = 'Device gms build                    : ' + get_prop_val(line)
            elif patt.device_kernel_build_user.search(line):
                device_kernel_build_user = 'Device product name                 : ' + get_prop_val(line)
            elif patt.device_security_patch_level.search(line):
                device_security_patch_level = 'Device product name                 : ' + get_prop_val(line)
            elif patt.device_slot_suffix.search(line):
                device_slot_suffix = 'Device product name                 : ' + get_prop_val(line)
            else:
                continue

        util.PLOGV(TAG,device_product_name)
        util.PLOGV(TAG,device_factory_serial_num)
        util.PLOGV(TAG,device_hw_serial_num)
        util.PLOGV(TAG,device_build_id)
        util.PLOGV(TAG,device_build_fingerprint)
        util.PLOGV(TAG,device_build_date)
        util.PLOGV(TAG,device_kernel_build_date)
        util.PLOGV(TAG,device_kernel_build_user)
        util.PLOGV(TAG,device_mpss_baseband1_build)
        util.PLOGV(TAG,device_mpss_baseband_build)
        util.PLOGV(TAG,device_gms_build)
        util.PLOGV(TAG,device_kernel_build_user)
        util.PLOGV(TAG,device_security_patch_level)
        util.PLOGV(TAG,device_slot_suffix)



        f_sys_prop.close()
        return True

    def extract_data_files():
        bool_ret = False
        try:
            f_bug_rpt = open(WS.file_bugreport,'rU')
        except IOError as err:
            err_str = 'failed to open file : ' + \
                WS.file_bugreport + '\n' + str(err)
            util.PLOGE(TAG, err_str)
            return False

        if not dump_build_details(f_bug_rpt):
            util.PLOGE(TAG, 'Failed to get build details')
        if not dump_kernel_logs(f_bug_rpt):
            util.PLOGE(TAG,'Failed to get kernel logs')
        if not dump_system_logs(f_bug_rpt):
            util.PLOGE(TAG,'Failed to get system logs')
        if not dump_event_logs(f_bug_rpt):
            util.PLOGE(TAG,'Failed to get events logs')
        if not dump_radio_logs(f_bug_rpt):
            util.PLOGE(TAG,'Failed to get radio logs')
        if not dump_sys_prop(f_bug_rpt):
            util.PLOGE(TAG,'Failed to get sys prop')

    extract_data_files()
    util.PLOGV(TAG, 'Exit   - analyze_bugreport')
    return True


def usage():
    util.print_empty_line()
    print util.prog_name + ' ' + '<options> ' + ' --file ' + ' bugreport.zip '
    util.print_line()
    print 'options:'
    print '\t-h,--help\t\t - print help'
    print '\t-v,--verbose\t\t - print verbose logging'
    print '\t--file <filename>\t - zip or txt file of bugreport'
    print '\t--out <out_dir>\t\t - output dir'
    print '\t--version\t\t - print version'
    util.print_empty_line()


def parse_argument(argv):
    long_opts = ['help', 'version', 'verbose', 'file=', 'out=']
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


def main():
    util.prog_name = sys.argv[0]
    if not parse_argument(sys.argv):
        util.PLOGE(TAG, 'parse argument failed', exit=True)
    start_analysis()


if __name__ == '__main__':
    main()
