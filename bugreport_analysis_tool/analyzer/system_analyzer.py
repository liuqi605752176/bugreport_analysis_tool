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
        util.PLOGE(TAG,errorString)
        return False

    f_native_crash_buf.write(util.get_line())
    f_native_crash_buf.write("--- Native crash ---")
    f_native_crash_buf.write(util.get_empty_line())
    f_native_crash_buf.write(util.get_line())
    f_native_crash_buf.write(util.get_empty_line())
    found_crash = False
    for line in f_system_log_buf:
        if pattr.start_crash_native.search(line):
            found_crash = True
            f_native_crash_buf.write(util.get_empty_line())
            f_native_crash_buf.write(util.get_line())
        if pattr.end_crash_native_conti.search(line):
            f_native_crash_buf.write(line)

    if not found_crash:
        f_native_crash_buf.write("Opps, No native crash")
        util.PLOGV(TAG,"Opps, No native crash")

    f_system_log_buf.close()
    f_native_crash_buf.close()
    return True

# Get Applicaton crashes
def GetAppCrashes(WS):
    try:
        f_system_log_buf = open(WS.file_system_logs,'r')
    except IOError as err:
        errorString = "failed to read system logs " + \
            str(err)
        util.PLOGE(errorString)
        return False

    try:
        f_app_crash_buf = open(WS.file_ws_system_app_crash,'w+')
    except IOError as err:
        errorString = 'failed to create application crash log file ' + \
            str(err)
        util.PLOGE(errorString)
        return False

    f_app_crash_buf.write(util.get_line())
    f_app_crash_buf.write("--- Application crash ---")
    f_app_crash_buf.write(util.get_empty_line())
    f_app_crash_buf.write(util.get_line())
    f_app_crash_buf.write(util.get_empty_line())
    found_crash = False
    for line in f_system_log_buf:
        if pattr.start_crash_application.search(line):
            found_crash = True
            f_app_crash_buf.write(util.get_empty_line())
            f_app_crash_buf.write(util.get_line())
        if pattr.end_crash_application.search(line):
            f_app_crash_buf.write(line)

    if not found_crash:
        f_app_crash_buf.write("Opps, No application crash")
        util.PLOGV(TAG,"Opps, No application crash")

    f_system_log_buf.close()
    f_app_crash_buf.close()

    return True

# Get ANR logs
# Get Applicaton crashes
def GetAppAnr(WS):
    try:
        f_system_log_buf = open(WS.file_system_logs,'r')
    except IOError as err:
        errorString = "failed to read system logs " + \
            str(err)
        util.PLOGE(errorString)
        return False

    try:
        f_app_anr_buf = open(WS.file_ws_system_anr,'w+')
    except IOError as err:
        errorString = 'failed to create application anr log file ' + \
            str(err)
        util.PLOGE(errorString)
        return False

    f_app_anr_buf.write(util.get_line())
    f_app_anr_buf.write("--- Application ANR ---")
    f_app_anr_buf.write(util.get_empty_line())
    f_app_anr_buf.write(util.get_line())
    f_app_anr_buf.write(util.get_empty_line())
    found_crash = False
    for line in f_system_log_buf:
        if pattr.start_anr_application.search(line):
            found_crash = True
            f_app_anr_buf.write(util.get_empty_line())
            f_app_anr_buf.write(util.get_line())
        if found_crash and pattr.end_anr_application.search(line):
            f_app_anr_buf.write(line)

    if not found_crash:
        f_app_anr_buf.write("Opps, No application ANR")
        util.PLOGV(TAG,"Opps, No application ANR")

    f_system_log_buf.close()
    f_app_anr_buf.close()

    return True