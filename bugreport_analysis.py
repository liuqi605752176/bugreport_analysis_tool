import sys
import os
import getopt
import utils as util
import config
import mimetypes
import zipfile
import shutil

'''
This is tool to get bugreport analysis

TODO:
1. Open bugreport from cmdline 
    - check , Is it zip or .txt
    - Extract if it is zip and open .txt 
2. Get build details for .txt file 
3. Display build details and device information 
4. Prepare CLI to shor the data as per user request
5. Add CLI option to short data with default configuration

Structure: 

bugreport_analysis/
|-- build_details.txt
`-- report.txt


command:
    bugreport_analysis.py -v --file bugreport.zip 

'''

#------------------------
# this
#-----------------------

# get options object and all config
OPT = util.OPT
debug_enable = config.MODE_DEBUG
test_enable = config.MODE_TEST
TAG  = 'bugreport_analysis'

def setup_ws():
    try:
        if os.path.exists(util.ws_out):
            shutil.rmtree(util.ws_out)
        os.makedirs(util.ws_out)
    except os.error as err:
        util.PLOGE(TAG,str(err),exit=False)
        return False
    return True
    
        


def prepare_bugreport_raw_data():
    if not setup_ws():
        util.PLOGE(TAG,'failed to setup ws',exit=False)
        return False
    
    is_unzip_required, error = util.is_unzip_required(OPT.zip_file)
    
    if error:
        util.PLOGE(TAG,'bugreport file type wrong, expected TEXT or ZIP ',exit=False)
        return False

    sys.path 
    if is_unzip_required:
        print ' Extracting ...'
        with zipfile.ZipFile(OPT.zip_file,'r') as bug_zip:
            try:
                bug_zip.extractall(util.ws_out)
            except zipfile.BadZipfile:
                util.PLOGE(TAG,'Badzipfile',exit=False)
                return False
            except zipfile.LargeZipFile:
                util.PLOGE(TAG,'LargeZipFile',exit=False)
                return False     
    return True

def check_prerequisite():
    if OPT.file_name is not None:
        OPT.zip_file = os.path.abspath(OPT.file_name)
        if not os.path.isfile(OPT.zip_file):
            util.PLOGE(TAG,'File not found or is not a file : ', OPT.zip_file ,exit=False)
            return False
       
        is_unzip_required, error = util.is_unzip_required(OPT.zip_file)
        
        if error:
            util.PLOGE(TAG,'bugreport file type wrong, expected TEXT or ZIP ',exit=False)
            return False
        
    return True

def usage():
    util.print_empty_line()
    print util.prog_name + ' ' + '<options> ' + ' --file ' + ' bugreport.zip '
    util.print_line()
    print 'options:'
    print '\t-h,--help\t\t - print help'
    print '\t-v,--verbose\t\t - print verbose logging'
    print '\t--file <filename>\t - zip or txt file of bugreport'
    print '\t--version\t\t - print version'
    util.print_empty_line()

def parse_argument(argv):
    long_opts = ['help','version','verbose','file=']
    short_opts = 'hvl'
    
    try : 
        opts_list, args_pos = getopt.getopt(argv[1:],short_opts,long_opts)
    except getopt.GetoptError:
        util.print_empty_line()
        print 'Error : args parser '
        usage()  
        sys.exit(1)

    if debug_enable:
        util.PLOGD(TAG,'opts are :',str(opts_list))
        util.PLOGD(TAG,'args are :',str(args_pos))

    if args_pos:
        usage()
        sys.exit(-1)

    for opt,val in opts_list:
        if opt == '--file':
            util.OPT.file_name = val
        elif opt in ['-h','--help']:
            usage()
            sys.exit(0)
        elif opt == '--version':
            print util.get_version()
            sys.exit(0)
        elif opt in ['-v','--verbose']:
            util.OPT.verbose = True
        else:
            print 'Error: wrong option : ' + opt
            sys.exit(0)

def start_analysis():
    # check cmd line args     
    if not check_prerequisite():
        usage()
        util.PLOGE(TAG,'check prerequitsite failed',exit=True)
    if not prepare_bugreport_raw_data():
        util.PLOGE(TAG,'Prepare bugreport data failed',exit=True)


def main():
    util.prog_name = sys.argv[0]
    parse_argument(sys.argv)
    start_analysis()

if __name__ == '__main__':
    main()


