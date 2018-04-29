import sys
import os
import getopt
import common as cmn

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

def usage():
    cmn.print_empty_line()
    print cmn.prog_name + ' ' + '<options> ' + ' --file ' + ' bugreport.zip '
    cmn.print_line()
    print 'options:'
    print '\t-h,--help\t\t - print help'
    print '\t-v,--verbose\t\t - print verbose logging'
    print '\t--file <filename>\t - zip or txt file of bugreport'
    print '\t--version\t\t - print version'
    cmn.print_empty_line()

def parse_argument(argv):
    long_opts = ['help','version','verbose','file=']
    short_opts = 'hvl'
    
    try : 
        opts_list, args_pos = getopt.getopt(argv[1:],short_opts,long_opts)
    except getopt.GetoptError:
        cmn.print_empty_line()
        print 'Error : args parser '
        usage()  
        sys.exit(1)

    cmn.print_line()
    print opts_list
    print args_pos
    cmn.print_line()

    file_name = None
    is_verbose = None
    
    for opt,val in opts_list:
        if opt == '--file':
            file_name = val
            
        elif opt in ['-h','--help']:
            usage()
            sys.exit(0)
        elif opt == '--version':
            print cmn.get_version()
            sys.exit(0)
        elif opt in ['-v','--verbose']:
            is_verbose = True
        else:
            print 'Error: wrong option : ' + opt
            sys.exit(0)

    print "We have got follwoing args : "
    print 'file name        : ' + file_name
    print 'Verbose loging   : ', is_verbose
    
def main():
    cmn.prog_name = sys.argv[0]
    parse_argument(sys.argv)
 
if __name__ == '__main__':
    main()


