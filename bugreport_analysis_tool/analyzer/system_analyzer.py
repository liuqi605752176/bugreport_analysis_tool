import sys
import buganalysis_utils as util
import filter as filt
import buganalysis_pattern as pattr
import os
import re

TAG = os.path.basename(__file__)
# WS = util.WS.file_system_logs
def GetNativeCrashes(WS):
    try:
        f_system_log_buf = open(WS.file_system_logs,'r')
    except IOError as err:
        errorString = "failed to read system logs " + \
            str(err)
        util.PLOGE(errorString)
        return False

    try:
        f_native_crash_buf = open(WS.file_ws_system_native_crash,'w+')
    except IOError as err:
        errorString = 'failed to create native crash log file ' + \
            str(err)
        util.PLOGE(errorString)
        return False

    f_native_crash_buf.write(util.get_line())
    f_native_crash_buf.write("--- Native crash ---")
    f_native_crash_buf.write(util.get_empty_line())
    f_native_crash_buf.write(util.get_line())
    f_native_crash_buf.write(util.get_empty_line())
    found_crash = False
    for line in f_system_log_buf:
        if pattr.crash_native_start.search(line):
            found_crash = True
            f_native_crash_buf.write(util.get_empty_line())
            f_native_crash_buf.write(util.get_line())
        if pattr.crash_native_conti_end.search(line):
            f_native_crash_buf.write(line)

    if not found_crash:
        f_native_crash_buf.write("Opps, No native crash")
        util.PLOGV(TAG,"Opps, No native crash")

    f_system_log_buf.close()
    f_native_crash_buf.close()

    return True
