import sys
import os
import getopt
import mimetypes
import zipfile
import shutil
import glob

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
    try:
        if os.path.exists(util.ws_out):
            shutil.rmtree(util.ws_out)
        os.makedirs(util.ws_out)
        os.makedirs(util.ws_analysis)
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
                bug_zip.extractall(util.ws_out)
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
        util.PLOGD(TAG,'bugreport zip file found : ' + str(is_unzip_required))

    return True


def set_files_path():
    files_list = glob.glob(util.ws_out + '/*')
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

    WS.file_build_details   = util.ws_analysis_build_details
    WS.file_system_logs     = util.ws_analysis_sys_logs
    WS.file_event_logs      = util.ws_analysis_event_logs
    WS.file_radio_logs      = util.ws_analysis_radio_logs
    WS.file_kernel_logs     = util.ws_analysis_kernel_logs

    util.PLOGV(TAG, WS.file_version)
    util.PLOGV(TAG, WS.file_dumpstate_log)
    util.PLOGV(TAG, WS.file_main_entry)
    util.PLOGV(TAG, WS.dir_FS)
    util.PLOGV(TAG, WS.file_bugreport)

    util.PLOGV(TAG,WS.file_build_details)
    util.PLOGV(TAG,WS.file_system_logs)
    util.PLOGV(TAG,WS.file_event_logs)
    util.PLOGV(TAG,WS.file_radio_logs)
    util.PLOGV(TAG,WS.file_kernel_logs)


    if not WS.file_bugreport:
        return False
    return True


def analyze_bugreport():
    # Get build details
    # Build: T5911INDURD-147 release-keys
    # Build fingerprint: 'Smartron/tphoneE/rimoE:8.1.0/T5911INDURD-147/147:user/release-keys'
    # Bootloader: unknown
    # Radio: MPSS.TA.2.3.c1-00605-8953_GEN_PACK-1.142704.1-Apr 24 2018
    # Network: , Jio 4G
    # # 1 SMP PREEMPT Tue Apr 24 01:19:21 IST 2018
    # Kernel: Linux version 3.18.71-perf(jenkins@tron6)(gcc version 4.9.x 20150123 (prerelease)(GCC))
    # Command line: sched_enable_hmp = 1 sched_enable_power_aware = 1 console = ttyHSL0, 115200, n8 androidboot.console = ttyHSL0 androidboot.hardware = qcom msm_rtb.filter = 0x237 ehci-hcd.park = 3 lpm_levels.sleep_disabled = 1 androidboot.bootdevice = 7824900.sdhci earlycon = msm_hsl_uart, 0x78af000 androidboot.selinux = permissive buildvariant = user androidboot.emmc = true androidboot.verifiedbootstate = green androidboot.veritymode = enforcing androidboot.keymaster = 1 androidboot.serialno = 4c4fc6c9 androidboot.authorized_kernel = true androidboot.baseband = msm mdss_mdp.panel = 1: dsi: 0: qcom, mdss_dsi_nt36672_1080p_hx_huashi_video: 1: none: cfg: single_dsi
    # Bugreport format version: 1.0
    # Dumpstate info: id = 1 pid = 5752 dry_run = 0 args = /system/bin/dumpstate - S - d - z - o / data/user_de/0/com.android.shell/files/bugreports/bugreport extra_options =
    print '-' * 80
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
    print '\t--version\t\t - print version'
    util.print_empty_line()


def parse_argument(argv):
    long_opts = ['help', 'version', 'verbose', 'file=']
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
