import os
import buganalysis_utils as util
import buganalysis_pattern as pattr
from analyzer import system_analyzer as system
from analyzer import event_analyzer as evnt
import re

'''
The buganalysis_analyzer module to analyze data and genrate report
'''
TAG = 'buganalysis_analyzer.py'

def StartEventAnaylzer(WS):
    evnt.start_event_log_analyzer(WS)

def StartSystemAnaylzer(WS):
    system.GetNativeCrashes(WS)
    system.GetAppCrashes(WS)
    system.GetAppAnr(WS)


