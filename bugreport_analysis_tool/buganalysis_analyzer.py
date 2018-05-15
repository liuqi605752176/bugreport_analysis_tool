import os
import buganalysis_utils as util
import buganalysis_filter as filter

WS = util.WS
'''
The buganalysis_analyzer module to analyze data and genrate report
'''
TAG = 'buganalysis_analyzer.py'

def clean_me(filename):
    if not os.path.isfile(filename):
        util.PLOGE(TAG,'file not found : ' + str(filename))
        return False
    os.remove(filename)
    return True

def start_event_log_analyzer(WS):
    filename = filter.get_file_with_filter_data(WS.file_event_logs,"am_proc_start")
    if (not filename) or not (os.path.isfile(filename)):
        util.PLOGE(TAG,'failed to set filter')
        return False

    try:
        f_buf = open(filename,'r')
    except IOError as err:
        util.PLOGE(TAG,'failed to read file : ' + str(err) )
        return False
    f_buf.close()
    util.dump_data_to_screen(TAG,filename)
    f_buf.close()
    clean_me(filename)





