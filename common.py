import sys
import os

prog_name = ''
ws_out = 'bugreport_analysis'
ws_build_details = 'build_details.txt'
ws_report = 'report.txt'

# version
major_ver = '1'
minor_ver = '01'




def print_line(symbol='-',len=90):
    print symbol * len

def print_empty_line():
    print ''

def get_version():
    version = 'Bugreport anaysis' + '- V' + major_ver + '.' + minor_ver
    return version
