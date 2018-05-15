import os
import buganalysis_utils as util
import tempfile as tmp
'''
The buganalysis_filter module to filter various data and return a tmp buf
or file buf
'''
TAG = 'buganalysis_filter.py'

def get_file_buf(pattern_string):
    try:
        f_tmp = tmp.NamedTemporaryFile(delete=False)
    except IOError as err:
        util.PLOGE(TAG,"failed to create tmp file : " + err )
    util.PLOGV(TAG,str(f_tmp.name))    
    return 1