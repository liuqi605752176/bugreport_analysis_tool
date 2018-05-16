import os
import buganalysis_utils as util
import tempfile as tmp
'''
The buganalysis_filter module to filter various data and return a tmp buf
or file buf
'''
TAG = 'buganalysis_filter.py'

def get_tmp_file():
    try:
        file_tmp = tmp.NamedTemporaryFile(delete=False)
    except IOError as err:
        util.PLOGE(TAG,"failed to create tmp file : " + err )
        return False
    util.PLOGV(TAG,str(file_tmp.name))
    return file_tmp.name

def get_file_with_filter_data(src_file,pattr):
    temp_file  = get_tmp_file()
    if not temp_file:
        util.PLOGE(TAG,'failed to get tmp file ')
        return False
    try:
        f_outfile = open(temp_file,'w+')
    except Exception as err:
        util.PLOGE(TAG,"failed to create file :  " + str(err) )
        return False
    with open(src_file,'rU') as f_event_log:
        for line in f_event_log:
            if not pattr.search(line):
                continue
            f_outfile.write(line)
        f_event_log.close()
    f_outfile.close()
    return temp_file