# dump file

import buganalysis_utils as util
import buganalysis_config as config
import buganalysis_pattern as patt
import buganalysis_dump as dump

TAG = 'buganalysis_dump'

def dump_build_details(WS,file_buf):
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
def dump_kernel_logs(WS,file_buf):
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
def dump_system_logs(WS,file_buf):
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
def dump_event_logs(WS,file_buf):
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
def dump_radio_logs(WS,file_buf):
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

# dump devinfo 
def dump_devinfo(WS,dict_devinfo):
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


def dump_sys_prop(WS,file_buf):

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

    if not dump_devinfo(WS,dict_devinfo):
        util.PLOGE(TAG, 'Failed to dump devinfo')

    return True

def extract_data_files(WS):
    try:
        f_bug_rpt = open(WS.file_bugreport,'rU')
    except IOError as err:
        err_str = 'failed to open file : ' + \
            WS.file_bugreport + '\n' + str(err)
        util.PLOGE(TAG, err_str)
        return False

    if not dump_build_details(WS,f_bug_rpt):
        util.PLOGE(TAG, 'Failed to get build details')
    if not dump_kernel_logs(WS,f_bug_rpt):
        util.PLOGE(TAG,'Failed to get kernel logs')
    if not dump_system_logs(WS,f_bug_rpt):
        util.PLOGE(TAG,'Failed to get system logs')
    if not dump_event_logs(WS,f_bug_rpt):
        util.PLOGE(TAG,'Failed to get events logs')
    if not dump_radio_logs(WS,f_bug_rpt):
        util.PLOGE(TAG,'Failed to get radio logs')
    if not dump_sys_prop(WS,f_bug_rpt):
        util.PLOGE(TAG,'Failed to get sys prop')
    return True