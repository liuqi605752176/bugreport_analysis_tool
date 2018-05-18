import os
import buganalysis_utils as util
import tempfile as tmp
import event_classes as bugClasses
import buganalysis_pattern as pattr
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

"""
04-25 11:42:23.412  root  2638  2638 I chatty  : uid=0(root) /vendor/bin/sh identical 7 lines
04-25 11:42:23.412  root  2638  2638 I auditd  : type=1400 audit(0.0:66): avc: denied { write } for comm="init.qcom.post_" name="b3000.dcc" dev="sysfs" ino=12833 scontext=u:r:qti_init_shell:s0 tcontext=u:object_r:sysfs:s0 tclass=dir permissive=0
04-25 11:42:23.462  root  2638  2638 I auditd  : type=1400 audit(0.0:67): avc: denied { write } for comm="init.qcom.post_" name="interactive" dev="sysfs" ino=38679 scontext=u:r:qti_init_shell:s0 tcontext=u:object_r:sysfs_devices_system_cpu:s0 tclass=dir permissive=0
04-25 11:42:23.757  1000  1656  1656 I am_uid_running: 10090
04-25 11:42:23.772  1000  1656  1656 I am_proc_start: [0,2701,10090,com.google.android.marvin.talkback,broadcast,com.google.android.marvin.talkback/com.google.android.accessibility.talkback.BootReceiver]
04-25 11:42:23.788  1000  1656  1888 I netstats_mobile_sample: [0,0,0,0,0,0,0,0,0,0,0,0,-1]
04-25 11:42:23.788  1000  1656  1888 I netstats_wifi_sample: [0,0,0,0,0,0,0,0,0,0,0,0,-1] """

def FilterByTagInFilesList(WS):
    '''
    - Open src_file and get list of tag from src_file
    - Sort lines with tag and make tmp files with tag name
    - retrun a list of files from actual dir
    '''
    # WS = util.WorkSpace()

    def getTag(tag,line):

        if not line:
            return False
        list_raw_words = str(line).split(': ')
        list_words = list_raw_words[0].split()
        tag.date = list_words[0]
        tag.time = list_words[1]
        tag.log_uid = list_words[2]
        tag.log_pid = list_words[3]
        tag.log_tid = list_words[4]
        tag.log_level = list_words[5]
        tag.tag_name = list_words[6]
        return True

    def WriteToFile(file,buf):
        try:
            f_buf = open(file,'a+')
        except IOError as err:
            util.PLOGE(TAG,'failed write file : ' + str(err))
            return False
        f_buf.write(buf)
        f_buf.close()
        return True

        ## get sort
    list_tag = []
    list_tag_files = []
    try:
        f_buf = open(WS.file_event_logs,'rU')
    except IOError as err:
        util.PLOGE(TAG,'failed read file : ' + str(err))
        return False

    ## skip title lines
    for each in [1,2,3]:
        f_buf.readline()


    for line in f_buf:
        if pattr.end_event_log.search(line):
            break
        mTag = bugClasses.Tag()
        # get the tag
        if not getTag(mTag,line):
            util.PLOGE(TAG,'failed to get tag', exit=False)
            return False

        if not mTag.tag_name in list_tag:
            list_tag.append(str(mTag.tag_name))

        if not mTag.tag_name in list_tag:
            continue

        file_name = os.path.abspath(WS.dir_ws_analysis_events + '/' + str(mTag.tag_name))
        if not file_name in list_tag_files:
            list_tag_files.append(file_name)

        if not WriteToFile(file_name,line):
            continue

    # util.dump_data_to_screen(TAG,list_tag)
    f_buf.close()
    return list_tag_files
