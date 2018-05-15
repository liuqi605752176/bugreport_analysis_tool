import os
import buganalysis_utils as util
import buganalysis_filter as filter
WS = util.WorkSpace()
'''
The buganalysis_analyzer module to analyze data and genrate report
'''
TAG = 'buganalysis_analyzer.py'

def start_event_log_analyzer(WS):
    filter.get_file_buf("am_proc_start")


