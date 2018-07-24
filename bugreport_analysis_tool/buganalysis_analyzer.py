import os
from analyzer import system_analyzer as system
from analyzer import event_analyzer as event

""" The buganalysis_analyzer module to analyze module wise logs
"""
TAG = os.path.basename(__file__)

def StartEventAnaylzer(WS):
    """Event logs anaylzer
    """
    event.StartAnalyzer(WS)

def StartSystemAnaylzer(WS):
    """System logs anaylzer
    """
    #Dump native crashes
    system.GetNativeCrashes(WS)

    #Dump application crashes
    system.GetAppCrashes(WS)

    #Dump application ANR
    system.GetAppAnr(WS)

    #Dump powerlogs
    system.DumpPowerLogs(WS)


