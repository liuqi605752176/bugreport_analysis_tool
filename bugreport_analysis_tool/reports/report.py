import os
import buganalysis_utils as util
import buganalysis_pattern as pattr
import re

TAG = os.path.basename(__file__)

def GenReport(WS):
    try:
        file_rpt = open(WS.file_analysis_rpt,'w+')
    except IOError as err:
        errstring = 'failed to create file ' + WS.file_analysis_rpt \
                    + ' Err: ' + str(err)
        util.PLOGE(errstring)
        return False

    util.PLOGV(TAG,util.OPT.bug_num)
    return True