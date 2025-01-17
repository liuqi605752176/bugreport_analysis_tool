import re

"""buganalysis_pattern module contain only regular expression pattern 
of various logs and tags 
"""

# Bugreport.zip file name pattern
pattern_version_file_wt_txt_ext         = re.compile(r'version.txt')
pattern_dumpstate_log_file_wt_txt_ext   = re.compile(r'dumpstate_log.txt')
pattern_main_entry_file_wt_txt_ext      = re.compile(r'main_entry.txt')
pattern_FS_dir                          = re.compile(r'/FS$')
pattern_bug_rpt_file_wt_txt_ext         = re.compile(r'[bugreport-]+.*[.](?=txt$)[^.]*$')


# bugreport.txt : bugreport tag pattern
start_of_file               = re.compile(r'^[==]+')

start_dumpsys_meminfo       = re.compile(r'^(------ DUMPSYS MEMINFO)')
end_dumsys_meminfo          = re.compile(r"('DUMPSYS MEMINFO' ------)$")
start_kernel_log            = re.compile(r'^(------ KERNEL LOG)')
end_kernel_log              = re.compile(r"(duration of 'KERNEL LOG)")
start_system_log            = re.compile(r'^(------ SYSTEM LOG)')
end_system_log              = re.compile(r"('SYSTEM LOG' ------)$")
start_event_log             = re.compile(r'^(------ EVENT LOG)')
end_event_log               = re.compile(r"('EVENT LOG' ------)$")
start_radio_log             = re.compile(r'^(------ RADIO LOG)')
end_radio_log               = re.compile(r"('RADIO LOG' ------)$")
start_sys_properties        = re.compile(r"^(------ SYSTEM PROPERTIES)")
end_sys_properties          = re.compile(r"('SYSTEM PROPERTIES' ------)$")
start_accounts              = re.compile(r'DUMP OF SERVICE account:')
end_accounts                = re.compile(r'the duration of dumpsys account')
start_uptime                = re.compile(r'------ UPTIME')
end_uptime                  = re.compile("the duration of 'UPTIME'")

#System properties pattern
device_product_name         = re.compile(r'(ro.product.name)')
device_factory_serial_num   = re.compile(r'(ro.serialno)[]]')
device_hw_serial_num        = re.compile(r'(ro.serialnohw)')
device_build_id             = re.compile(r'(ro.build.display.id)')
device_build_fingerprint    = re.compile(r'(ro.build.fingerprint)')
device_build_date           = re.compile(r'(ro.build.date)[]]')
device_kernel_build_date    = re.compile(r'(ro.bootimage.build.date)[]]')
device_kernel_build_user    = re.compile(r'(ro.build.user)')
device_mpss_baseband_build  = re.compile(r'(gsm.version.baseband)')
device_mpss_baseband1_build = re.compile(r'(gsm.version.baseband1)')
device_gms_build            = re.compile(r'(ro.com.google.gmsversion)')
device_security_patch_level = re.compile(r'(ro.build.version.security_patch)')
device_slot_suffix          = re.compile(r'(ro.boot.slot_suffix)')

# avc log pattern
pattern_avc = 'avc:'
pattern_denied = 'denied'
pattern_comm = 'comm='
pattern_name = 'name='

# Event logs activity manager log pattern
am_proc_start = re.compile('am_proc_start:')
am_proc_died  = re.compile('am_proc_died:')
am_proc_bound = re.compile('am_proc_died:')

# Event logs power screen on and off pattern
screen_off      = re.compile(r'screen_toggled: 0')
screen_on       = re.compile(r'screen_toggled: 1')

# System logs native crash pattern
start_crash_native          = re.compile(r'F DEBUG   : [*]+')
end_crash_native_conti      = re.compile('F DEBUG   :')

# System logs application crash pattern
start_crash_application     = re.compile(r'E AndroidRuntime: FATAL EXCEPTION:')
end_crash_application       = re.compile(r'E AndroidRuntime:')

# System logs application ANR pattern
start_anr_application       = re.compile(r'E ActivityManager: ANR in')
end_anr_application         = re.compile(r'E ActivityManager: ')
start_anr_all               = re.compile(r'------ VM TRACES JUST NOW')
# The anr dump in bugreport consist two type VM TRACES
# 1. VM TRACES JUST NOW          --- from live device
# 2. VM TRACES AT LAST ANR       --- from /data/anr/
# The 2nd tag doesn't have 'end' tag, So will dump TRACES
# till next new tag found i.e 'NETWORK DEV INFO'
end_anr_all                 = re.compile(r"------ NETWORK DEV INFO")



# System logs process start pattern
start_proc                  = re.compile(r'ActivityManager: Start proc')

# System log Power manager pattern
device_sys_sleep_power_button   = re.compile(r'PowerManagerService: Going to sleep due to power button')
device_sys_sleep_screen_timeout = re.compile(r'PowerManagerService: Going to sleep due to screen timeout')
device_sys_wake_up              = re.compile(r'PowerManagerService: Waking up from dozing')

# Kernel log Power manager pattern
device_kernel_sleep             = re.compile(r'PM: suspend entry')
device_kernel_wakeup            = re.compile(r'PM: suspend exit')

# Bugreport start pattern
start_bugreport_sys                 = re.compile(r'dumpstate: begin')
start_bugreport_kernel              = re.compile(r"init: starting service 'dumpstatez'")

#-Bugreport PID mapping pattern
start_PID_mapping               = re.compile(r'PID mappings:')
end_PID_mapping_conti           = re.compile(r'PID #')

