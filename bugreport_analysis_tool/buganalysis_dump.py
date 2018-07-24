import buganalysis_utils as util
import buganalysis_pattern as patt
import os
""" bugnanalysis_dump module to dump various log in to 
    seperate files 
"""

TAG = os.path.basename(__file__)

def DumpBuildDetails(WS,file_buf):
    """Dump build details
    """
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
def DumpKernelLogs(WS,file_buf):
    """Dump kernel logs
    """
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
def DumpSystemLogs(WS,file_buf):
    """ Dump system logs
    """
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

# TODO: optimise in single function
def DumpEventLogs(WS,file_buf):
    """Dump event logs
    """
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
def DumpRadioLogs(WS,file_buf):
    """ Dump radio logs
    """
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


def DumpDevinfo(WS,dict_devinfo):
    """Dump device information
    """
    try:
        f_devinfo = open(WS.file_devinfo, 'w+')
    except IOError as err:
        err_str = 'failed to create file : ' + WS.file_devinfo + \
                  str(err)
        util.PLOGE(TAG,err_str)
        return False

    f_devinfo.write(util.get_line())
    f_devinfo.write('--- devinfo ---\n')
    f_devinfo.write(util.get_line())

    for item in dict_devinfo:
        f_devinfo.write(util.get_empty_line())
        f_devinfo.write(dict_devinfo[item])

    f_devinfo.write(util.get_empty_line())
    f_devinfo.close()
    return True


def DumpSysProp(WS,file_buf):
    """Dump system properties
    """
    def get_prop_val(prop):
        list_prop_val = str(prop).split(': [')
        # print list_prop_val
        return list_prop_val[1].strip('\n').strip(']')

    bool_start_dump = False

    try:
        f_sys_prop = open(WS.file_sys_prop, 'w+')
    except IOError as err:
        err_str = 'failed to create file : ' + WS.file_sys_prop + \
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
    dict_devinfo = {
        'device_product_name' : '',
        'device_factory_serial_num' : '',
        'device_hw_serial_num' : '',
        'device_build_id' : '',
        'device_build_fingerprint' : '',
        'device_build_date' : '',
        'device_kernel_build_date' : '',
        'device_kernel_build_user' : '',
        'device_mpss_baseband1_build' : '',
        'device_mpss_baseband_build' : '',
        'device_gms_build' : '',
        'device_kernel_build_user' : '',
        'device_security_patch_level' : '',
        'device_slot_suffix' : ''
    }

    for line in f_sys_prop:
        if patt.device_product_name.search(line):
            dict_devinfo['device_product_name'] = 'Device product name                 : ' + get_prop_val(line)
        elif patt.device_factory_serial_num.search(line):
            dict_devinfo['device_factory_serial_num'] = 'Device factory serial number        : ' + get_prop_val(line)
        elif patt.device_hw_serial_num.search(line):
            dict_devinfo['device_hw_serial_num'] = 'Device hardware serial number name  : ' + get_prop_val(line)
        elif patt.device_build_id.search(line):
            dict_devinfo['device_build_id'] = 'Device build id                     : ' + get_prop_val(line)
        elif patt.device_build_fingerprint.search(line):
            dict_devinfo['device_build_fingerprint'] = 'Device build fingerprint            : ' + get_prop_val(line)
        elif patt.device_build_date.search(line):
            dict_devinfo['device_build_date'] = 'Device build date                   : ' + get_prop_val(line)
        elif patt.device_kernel_build_date.search(line):
            dict_devinfo['device_kernel_build_date'] = 'Device kernel build date            : ' + get_prop_val(line)
        elif patt.device_kernel_build_user.search(line):
            dict_devinfo['device_kernel_build_user'] = 'Device kernel build user            : ' + get_prop_val(line)
        elif patt.device_mpss_baseband1_build.search(line):
            dict_devinfo['device_mpss_baseband1_build']= 'Device mpss baseband1 build         : ' + get_prop_val(line)
        elif patt.device_mpss_baseband_build.search(line):
            dict_devinfo['device_mpss_baseband_build'] = 'Device mpss baseband build          : ' + get_prop_val(line)
        elif patt.device_gms_build.search(line):
            dict_devinfo['device_gms_build'] = 'Device gms build                    : ' + get_prop_val(line)
        elif patt.device_kernel_build_user.search(line):
            dict_devinfo['device_kernel_build_user'] = 'Device product name                 : ' + get_prop_val(line)
        elif patt.device_security_patch_level.search(line):
            dict_devinfo['device_security_patch_level'] = 'Device product name                 : ' + get_prop_val(line)
        elif patt.device_slot_suffix.search(line):
            dict_devinfo['device_slot_suffix'] = 'Device product name                 : ' + get_prop_val(line)
        else:
            continue

    f_sys_prop.close()

    util.PLOGV(TAG,dict_devinfo['device_product_name'])
    util.PLOGV(TAG,dict_devinfo['device_factory_serial_num'])
    util.PLOGV(TAG,dict_devinfo['device_hw_serial_num'])
    util.PLOGV(TAG,dict_devinfo['device_build_id'])
    util.PLOGV(TAG,dict_devinfo['device_build_fingerprint'])
    util.PLOGV(TAG,dict_devinfo['device_build_date'])
    util.PLOGV(TAG,dict_devinfo['device_kernel_build_date'])
    util.PLOGV(TAG,dict_devinfo['device_kernel_build_user'])
    util.PLOGV(TAG,dict_devinfo['device_mpss_baseband1_build'])
    util.PLOGV(TAG,dict_devinfo['device_mpss_baseband_build'])
    util.PLOGV(TAG,dict_devinfo['device_gms_build'])
    util.PLOGV(TAG,dict_devinfo['device_kernel_build_user'])
    util.PLOGV(TAG,dict_devinfo['device_security_patch_level'])
    util.PLOGV(TAG,dict_devinfo['device_slot_suffix'])

    if not DumpDevinfo(WS,dict_devinfo):
        util.PLOGE(TAG, 'Failed to dump devinfo')

    return True

def DumpAccounts(WS,file_buf):
    """Dump Account information
    """
    bool_start_dump = False
    try:
        f_accounts = open(WS.file_accounts, 'w+')
    except IOError as err:
        err_str = 'failed to create file : ' + WS.file_accounts + \
                  '\n' + str(err)
        util.PLOGE(TAG, err_str)
        return False

    f_accounts.write(util.get_line())
    f_accounts.write('--- Accounts ---\n')
    f_accounts.write(util.get_line())

    for line in file_buf:
        if bool_start_dump:
            f_accounts.write(line)
        if patt.start_accounts.search(line):
            bool_start_dump = True
        if patt.end_accounts.search(line):
            bool_start_dump = False
            break

    f_accounts.write(util.get_empty_line())
    f_accounts.close()
    return True

def DumpUptime(WS,file_buf):
    """Dump uptime
    """
    bool_start_dump = False
    try:
        f_other = open(WS.file_other, 'w+')
    except IOError as err:
        err_str = 'failed to create file : ' + WS.file_accounts + \
                  '\n' + str(err)
        util.PLOGE(TAG, err_str)
        return False

    f_other.write(util.get_line())
    f_other.write('--- Other ---\n')
    f_other.write(util.get_line())
    f_other.write(util.get_empty_line())

    for line in file_buf:
        if bool_start_dump:
            f_other.write(line)
        if patt.start_uptime.search(line):
            f_other.write(line)
            bool_start_dump = True
        if patt.end_uptime.search(line):
            bool_start_dump = False
            break

    f_other.write(util.get_empty_line())
    f_other.close()
    return True

def ExtractLogs(WS):
    """Extract data files
    """
    try:
        f_bug_rpt = open(WS.file_bugreport,'rU')
    except IOError as err:
        err_str = 'failed to open file : ' + \
                  WS.file_bugreport + '\n' + str(err)
        util.PLOGE(TAG, err_str)
        return False

    if not DumpBuildDetails(WS,f_bug_rpt):
        util.PLOGE(TAG, 'Failed to get build details')
    if not DumpUptime(WS, f_bug_rpt):
        util.PLOGE(TAG, 'Failed to get uptime logs')
    if not DumpKernelLogs(WS,f_bug_rpt):
        util.PLOGE(TAG,'Failed to get kernel logs')
    if not DumpSystemLogs(WS,f_bug_rpt):
        util.PLOGE(TAG,'Failed to get system logs')
    if not DumpEventLogs(WS,f_bug_rpt):
        util.PLOGE(TAG,'Failed to get events logs')
    if not DumpRadioLogs(WS,f_bug_rpt):
        util.PLOGE(TAG,'Failed to get radio logs')
    if not DumpSysProp(WS,f_bug_rpt):
        util.PLOGE(TAG,'Failed to get sys prop')
    if not DumpAccounts(WS,f_bug_rpt):
        util.PLOGE(TAG,'failed to get account details')
    return True

def FilterAvcLogs(WS):
    """Filter out acv denied logs
    """
    AVC_PATTERN = patt.pattern_avc
    DENIED_PATTERN = patt.pattern_denied
    COMM_PATTERN = patt.pattern_comm
    NAME_PATTERN = patt.pattern_name

    comm_list = []
    name_list = []
    scontext_list = []
    temp_avc_file = '/tmp/temp_avc_file.txt'
    TAG = 'dump_avc.py'

    def AvcLogs(WS):
        """FilterAvcLogs :
            filter avc denied
        """
        try:
            sys_log_buf = open(WS.file_event_logs, 'rU')
        except IOError as err:
            err_string = 'failed to read : ' + WS.file_system_logs + \
                         'error : ' + err
            util.PLOGE(TAG,err_string)
            return False

        try:
            f_tmp_avc = open(temp_avc_file,'w+')
        except IOError:
            util.PLOGE(TAG,'failed to create : ' + temp_avc_file)
            return False

        for line in sys_log_buf:
            if not AVC_PATTERN in line:
                continue
            if not DENIED_PATTERN in line:
                continue
            if COMM_PATTERN in line or NAME_PATTERN in line:
                f_tmp_avc.write(line)
                split_list = line.split()
                for word in split_list:
                    data = []
                    if 'comm=' in word or 'name=' in word:
                        data = word.split('=')
                        data[1] = data[1].strip('"')
                        if data[0] == 'comm':
                            if data[1] not in comm_list:
                                comm_list.append(data[1])
                        elif data[0] == 'name':
                            if data[1] not in name_list:
                                name_list.append(data[1])

                    if 'scontext=' in word:
                        data = word.split(':')
                        if data[2] not in scontext_list:
                            scontext_list.append(data[2])

        sys_log_buf.close()
        f_tmp_avc.close()
        return comm_list, scontext_list


    def WriteToFile(WS):
        """FilterAvcLogs
            Dump filtered avc logs in to file
        """
        dash_line = '-' * 90 + '\n'
        if os.path.isfile(WS.file_avc_logs):
            os.remove(WS.file_avc_logs)
        f = open(WS.file_avc_logs, 'a+')

        f.write(dash_line)
        f.write('\t' + 'comm' + '\n')
        f.write(dash_line)
        for cmd in comm_list:
            f.write(cmd + '\n')
        f.write('\n')

        f.write(dash_line)
        f.write('\t' + 'name' + '\n')
        f.write(dash_line)
        for cmd in name_list:
            f.write(cmd + '\n')
        f.write('\n')


        f.write(dash_line)
        f.write('\t' + 'scontext' + '\n')
        f.write(dash_line)
        for scontext in scontext_list:
            f.write(scontext + '\n')
        f.write('\n')

        f.write(dash_line)
        f.write('\t' + 'Logs' + '\n')
        f.write(dash_line)

        avc_count = 1
        for cmd in comm_list:
            f.write(' \n')
            f.write(cmd + ' \n')
            f.write(dash_line)

            logcat_buf = open(temp_avc_file, 'rU')

            for line in logcat_buf:
                if AVC_PATTERN in line and DENIED_PATTERN in line and COMM_PATTERN in line:
                    if cmd in line:
                        f.write(line)

            f.write(' \n')
            logcat_buf.close()
            avc_count += 1

        f.close()
        avc_summary = str(avc_count) + ' : type of avc logs found'
        util.PLOGV(TAG,avc_summary)

    # Start avc filter
    AvcLogs(WS)
    WriteToFile(WS)
