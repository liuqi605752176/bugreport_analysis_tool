import re


pattern_version_file_wt_txt_ext = re.compile(
    r'version.txt')
pattern_dumpstate_log_file_wt_txt_ext = re.compile(
    r'dumpstate_log.txt')
pattern_main_entry_file_wt_txt_ext = re.compile(
    r'main_entry.txt')
pattern_FS_dir = re.compile(r'/FS$')
pattern_bug_rpt_file_wt_txt_ext = re.compile(
    r'[bugreport-]+.*[.](?=txt$)[^.]*$')


#############################################
# Bugreport TAG pattern
############################################

# dumpsys meminfo
start_of_file = re.compile(r'^[==]+')
start_dumpsys_meminfo = re.compile(r'^(------ DUMPSYS MEMINFO)')
end_dumsys_meminfo = re.compile(r"('DUMPSYS MEMINFO' ------)$")

start_kernel_log = re.compile(r'^(------ KERNEL LOG)')
end_kernel_log = re.compile(r"(duration of 'KERNEL LOG)")
start_system_log = re.compile(r'^(------ SYSTEM LOG)')
end_system_log = re.compile(r"('SYSTEM LOG' ------)$")
start_event_log = re.compile(r'^(------ EVENT LOG)')
end_event_log = re.compile(r"('EVENT LOG' ------)$")
start_radio_log = re.compile(r'^(------ RADIO LOG)')
end_radio_log = re.compile(r"('RADIO LOG' ------)$")


# ------ 0.656s was the duration of 'SYSTEM LOG' - -----
# ------ 0.116s was the duration of 'EVENT LOG' - -----
# ------ 0.288s was the duration of 'RADIO LOG' - -----
# ------ 0.006s was the duration of 'KERNEL LOG (dmesg)' - -----
