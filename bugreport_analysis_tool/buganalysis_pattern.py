import re


pattern_version_file_wt_txt_ext         = re.compile(r'version.txt')
pattern_dumpstate_log_file_wt_txt_ext   = re.compile(r'dumpstate_log.txt')
pattern_main_entry_file_wt_txt_ext      = re.compile(r'main_entry.txt')
pattern_FS_dir                          = re.compile(r'/FS$')
pattern_bug_rpt_file_wt_txt_ext         = re.compile(r'[bugreport-]+.*[.](?=txt$)[^.]*$')


#############################################
# Bugreport TAG pattern
############################################

# dumpsys meminfo
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


#############################################
# system prop TAG pattern
############################################

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



