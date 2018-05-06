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
