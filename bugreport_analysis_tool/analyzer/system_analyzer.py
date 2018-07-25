import buganalysis_utils as util
import buganalysis_pattern as pattr
import os

"""system_analyzer.py class to analyze system logs
"""

TAG = os.path.basename(__file__)

def GetNativeCrashes(WS):
    """Dump native crash logs

    :param WS: WorkSpace object
    :return: True on Success and False on Failure
    """
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

def GetAppCrashes(WS):
    """Dump application crash logs

    :param WS: WorkSpace object
    :return: True on Success and False on Failure
    """
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


def GetAppAnr(WS):
    """Dump application ANR logs

    :param WS: WorkSpace object
    :return: True on Success and False on Failure
    """
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

def DumpPowerLogs(WS):
    """Dump power logs

    :param WS: WorkSpace object
    :return: True on Success and False on Failure
    """
    try:
        f_power_logs_buf = open(WS.file_power_logs, 'a+')
    except IOError as err:
        error = 'failed to create power log file : ' + str(err)
        util.PLOGE(TAG, error)
        return False

    try:
        f_sys_logs_buf = open(WS.file_system_logs, 'r')
    except IOError as err:
        error = 'failed to read event log file : ' + str(err)
        util.PLOGE(TAG, error)
        return False

    try:
        f_kernel_logs_buf = open(WS.file_kernel_logs, 'r')
    except IOError as err:
        error = 'failed to read event log file : ' + str(err)
        util.PLOGE(TAG, error)
        return False

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
    return True

