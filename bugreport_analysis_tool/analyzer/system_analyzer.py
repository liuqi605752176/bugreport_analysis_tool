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

    f_system_log_buf.close()
    f_native_crash_buf.close()

    if not found_crash:
        os.remove(WS.file_ws_system_native_crash)
        util.PLOGV(TAG,"Opps, No native crash")

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


    f_system_log_buf.close()
    f_app_crash_buf.close()

    if not found_crash:
        os.remove(WS.file_ws_system_app_crash)
        util.PLOGV(TAG,"Opps, No application crash")

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

    f_system_log_buf.close()
    f_app_anr_buf.close()

    if not found_crash:
        os.remove(WS.file_ws_system_anr)
        util.PLOGV(TAG,"Opps, No application ANR")

    return True

# Dump power logs:
# device_sys_sleep_power_button
# device_sys_sleep_screen_timeout
# device_sys_wake_up
# device_kernel_sleep
# device_kernel_wakeup
def DumpPowerLogs(WS):
    try:
        f_power_logs_buf = open(WS.file_ws_analysis_power_logs, 'a+')
    except IOError as err:
        error = 'failed to create power log file : ' + str(err)
        util.PLOGE(TAG, error)

    try:
        f_sys_logs_buf = open(WS.file_system_logs, 'r')
    except IOError as err:
        error = 'failed to read event log file : ' + str(err)
        util.PLOGE(TAG, error)

    try:
        f_kernel_logs_buf = open(WS.file_kernel_logs, 'r')
    except IOError as err:
        error = 'failed to read event log file : ' + str(err)
        util.PLOGE(TAG, error)

    f_power_logs_buf.write('--- PowerManager ---')
    f_power_logs_buf.write(util.get_empty_line())
    f_power_logs_buf.write(util.get_empty_line())

    for line in f_sys_logs_buf:
        if pattr.device_sys_sleep_power_button.search(line) or \
                pattr.device_sys_sleep_screen_timeout.search(line) or \
                pattr.device_sys_wake_up.search(line):
            f_power_logs_buf.write(line)
    f_power_logs_buf.write(util.get_empty_line())

    f_power_logs_buf.write('--- Kernel ---')
    f_power_logs_buf.write(util.get_empty_line())
    f_power_logs_buf.write(util.get_empty_line())


    for line in f_kernel_logs_buf:
        if pattr.device_kernel_sleep.search(line) or \
                pattr.device_sys_sleep_screen_timeout.search(line) or \
                pattr.device_kernel_wakeup.search(line):
            f_power_logs_buf.write(line)
    f_power_logs_buf.write(util.get_empty_line())

    f_power_logs_buf.close()
    f_sys_logs_buf.close()
    f_kernel_logs_buf.close()

