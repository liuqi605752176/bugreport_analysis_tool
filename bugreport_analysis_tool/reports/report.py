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
        WriteTitleAndValue('Device info', ' --->>>')
        with open(WS.file_devinfo,'r') as device:
            for line in device:
                if re.compile(r'Device ').search(line):
                    keyValue = line.split(': ')
                    mFile_rpt_buf.write(keyValue[0].strip())
                    mFile_rpt_buf.write(str(' ' * (30 - len(keyValue[0].strip()))))
                    mFile_rpt_buf.write(': ')
                    mFile_rpt_buf.write(keyValue[1])
        device.close()

    def WriteDeviceAccount():
        acc_list = []
        with open(WS.file_system_logs, 'r') as system:
            for line in system:
                email_match = re.search(r'([\w.-]+)@([\w.-]+)', line)
                acc_list.append(email_match.group())

    ## Dump report
    WriteReportTitle()
    WriteBugID()
    WriteBugTitle()
    WriteDevEngineer()
    WriteTestEngineer()
    WriteBuildDetails()
    WriteDeviceDetails()


    return True
    
