import os
import buganalysis_utils as util
import buganalysis_pattern as pattr
import re

TAG = os.path.basename(__file__)

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
# Native crash :
# Application Crash :
# Application ANR :



def GenReport(WS):
    try:
        mFile_rpt_buf = open(WS.file_analysis_rpt, 'w+')
    except IOError as err:
        errstring = 'failed to create file ' + WS.file_analysis_rpt \
                    + ' Err: ' + str(err)
        util.PLOGE(errstring)
        return False
        
    def WriteReportTitle():
        mFile_rpt_buf.write(util.get_line())
        mFile_rpt_buf.write('BUGREPORT ANALYSIS')
        mFile_rpt_buf.write(util.get_empty_line())
        mFile_rpt_buf.write(util.get_line())
        mFile_rpt_buf.write(util.get_empty_line())
        mFile_rpt_buf.write(util.get_empty_line())

    def PreapreTitle(title):
        return title + ' ' * (30 - len(title) ) + ': '

    def WriteTitleAndValue(title,value):
        mFile_rpt_buf.write(str(PreapreTitle(title)))
        mFile_rpt_buf.write(str(value))
        mFile_rpt_buf.write(util.get_empty_line())

    def WriteBugID():
        WriteTitleAndValue('Bug ID',util.OPT.bug_num)

    def WriteBugTitle():
        WriteTitleAndValue('Bug title',util.OPT.bug_title)

    def WriteDevEngineer():
        if util.OPT.dev_name is None:
            util.OPT.dev_name = os.getlogin()
        WriteTitleAndValue('Dev Enginner',util.OPT.dev_name)

    def WriteTestEngineer():
        WriteTitleAndValue('Test Enginner',util.OPT.tester_name)

    def WriteBuildDetails():
        build_id=None
        with open(WS.file_build_details,'r') as build:
            for line in build:
                if re.compile(r'Build:').search(line):
                    build_id = line.split(':').pop(1)
                    break
        build.close()
        WriteTitleAndValue('Build ID',build_id[1:])

    def WriteDeviceDetails():
        WriteTitleAndValue('Device info', '--->>>')
        with open(WS.file_devinfo,'r') as device:
            for line in device:
                if re.compile(r'Device ').search(line):
                    keyValue = line.split(': ')
                    mFile_rpt_buf.write(keyValue[0].strip())
                    mFile_rpt_buf.write(str(' ' * (30 - len(keyValue[0].strip()))))
                    mFile_rpt_buf.write(': ')
                    mFile_rpt_buf.write(keyValue[1])
        device.close()

    def WriteDeviceOwnerAndAccount():
        user = None
        acc_list = []
        with open(WS.file_accounts, 'r') as system:
            for line in system:
                email_match = re.search(r'([\w.-]+)@([\w.-]+)', line)
                if email_match:
                    if email_match.group() not in acc_list:
                        acc_list.append(email_match.group())
                if re.compile(r'UserInfo').search(line):
                    user=line.split(':')[1]
        WriteTitleAndValue('Device onwer',user)
        WriteTitleAndValue('Device Accounts','--->>>')
        for account in acc_list:
            mFile_rpt_buf.write((' ' * 32)  + account)
            mFile_rpt_buf.write(util.get_empty_line())

        system.close()

    def WriteUptime():
        uptime = None
        uptime_found = False
        with open(WS.file_other, 'r') as other:
            for line in other:
                if uptime_found:
                    uptime = line.split(',').pop(0).strip()
                    break
                if pattr.start_uptime.search(line):
                    uptime_found = True

        print uptime
        WriteTitleAndValue('Up time',uptime)
        other.close()

    def WriteNetwork():
        network=None
        with open(WS.file_build_details,'r') as build:
            for line in build:
                if re.compile(r'Network:').search(line):
                    network = line.split(':').pop(1)
                    break
        build.close()
        WriteTitleAndValue('Network',network[1:])
    #
    # util.PrintTerminalLink(WS.file_ws_system_native_crash)
    # util.PrintTerminalLink(WS.file_ws_system_app_crash)
    # util.PrintTerminalLink(WS.file_ws_system_anr)
    def WriteNativeCrash():
        native_crash = False
        native_crash_list = []
        cont = False
        if os.path.exists(WS.file_ws_system_native_crash):
            with open(WS.file_ws_system_native_crash) as native_crash_buf:
                for line in native_crash_buf:
                    if cont or re.compile('F DEBUG   : pid:').search(line):
                        native_crash = True
                        cont = True
                        native_crash_list.append(line)
                    if re.compile('F DEBUG   : Abort message:').search(line):
                        native_crash_list.append('#')
                        cont = False
                WriteTitleAndValue('Native crash', '--->>>')
                mFile_rpt_buf.write(util.get_line())

                for item in native_crash_list:
                    if item == '#':
                        mFile_rpt_buf.write(util.get_empty_line())
                        continue
                    mFile_rpt_buf.write(item)

                native_crash_buf.close()

        if not native_crash :
            WriteTitleAndValue('Native crash','None')
            mFile_rpt_buf.write(util.get_line())
            return



    def WriteApplicationCrash():
        app_crash = None
        app_crash_list = []
        cont = False
        if os.path.exists(WS.file_ws_system_app_crash):
            with open(WS.file_ws_system_app_crash) as app_crash_buf:
                for line in app_crash_buf:
                    if cont or re.compile('E AndroidRuntime: FATAL EXCEPTION:').search(line):
                        app_crash = True
                        cont = True
                        app_crash_list.append(line)
                    if re.compile('E AndroidRuntime: android.os.').search(line) or \
                            re.compile('E AndroidRuntime: java.lang.').search(line):
                        app_crash_list.append('#')
                        cont = False

            WriteTitleAndValue('Application crash','--->>>')
            mFile_rpt_buf.write(util.get_line())

            if app_crash is not None:
                for item in app_crash_list:
                    if item == '#':
                        mFile_rpt_buf.write(util.get_empty_line())
                        continue
                    mFile_rpt_buf.write(item)

            app_crash_buf.close()

        if app_crash is None:
            WriteTitleAndValue('Application crash',app_crash)
            mFile_rpt_buf.write(util.get_line())
            return

    def WriteApplicationAnr():
        app_anr = None
        app_anr_list = []
        cont = False
        if os.path.exists(WS.file_ws_system_anr):
            with open(WS.file_ws_system_anr) as app_anr_buf:
                for line in app_anr_buf:
                    if cont or re.compile('E ActivityManager: ANR in ').search(line):
                        app_anr = True
                        cont = True
                        app_anr_list.append(line)
                    if re.compile('E ActivityManager: Reason: ').search(line):
                        app_anr_list.append('#')
                        cont = False

            WriteTitleAndValue('Application ANR','--->>>')
            mFile_rpt_buf.write(util.get_line())

            if app_anr is not None:
                for item in app_anr_list:
                    if item == '#':
                        mFile_rpt_buf.write(util.get_empty_line())
                        continue
                    mFile_rpt_buf.write(item)

            app_anr_buf.close()

        if app_anr is None:
            WriteTitleAndValue('Application ANR',app_anr)
            mFile_rpt_buf.write(util.get_line())
            return


    ## Dump report
    WriteReportTitle()
    # WriteBugID()
    WriteBugTitle()
    WriteDevEngineer()
    WriteTestEngineer()
    WriteBuildDetails()
    WriteDeviceDetails()
    WriteDeviceOwnerAndAccount()
    WriteUptime()
    WriteNetwork()
    WriteNativeCrash()
    WriteApplicationCrash()
    WriteApplicationAnr()


    return True
    
