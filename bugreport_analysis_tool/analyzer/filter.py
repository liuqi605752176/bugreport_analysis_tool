import os
import buganalysis_utils as util
import tempfile as tmp
import event_classes as bugClasses
import buganalysis_pattern as pattr
"""filter.py module has various filters for logs
"""

TAG = os.path.basename(__file__)

def GetTempFile():
    """Create temp file and open it and return fd.
    """
    try:
        file_tmp = tmp.NamedTemporaryFile(delete=False)
    except IOError as err:
        util.PLOGE(TAG,"failed to create tmp file : " + err )
        return False
    util.PLOGV(TAG,str(file_tmp.name))
    return file_tmp.name

def GetFileWithFilterData(src_file,pattr):
    """ Filter file data with given pattern
    :param src_file: file to be filter
    :param pattr: filter pattern
    :return: filtered content in file format
    """
    temp_file  = GetTempFile()
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

def FilterByTagInFilesList(WS):
    """Extract the event log tags and create file of each tag
    with filtered data by that tag

    :param WS: workspace object
    :return: List of tags in event log
    """
    def GetTag(tag,line):
        """ Fill tag object from line content

        :param tag: Tag class object
        :param line: event log line
        :return: None
        """
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
        """Write given buffer to given file

        :param file: File name
        :param buf: data to be write
        :return: True on Success and False on Failure
        """
        try:
            f_buf = open(file,'a+')
        except IOError as err:
            util.PLOGE(TAG,'failed write file : ' + str(err))
            return False
        f_buf.write(buf)
        f_buf.close()
        return True

    # Get list tag from event log
    list_tag = []
    list_tag_files = []
    try:
        f_buf = open(WS.file_event_logs,'rU')
    except IOError as err:
        util.PLOGE(TAG,'failed read file : ' + str(err))
        return False

    # skip title lines
    for each in [1,2,3]:
        f_buf.readline()


    for line in f_buf:
        if pattr.end_event_log.search(line):
            break
        mTag = bugClasses.Tag()
        # get the tag
        if not GetTag(mTag,line):
            util.PLOGE(TAG,'failed to get tag', exit=False)
            return False

        if not mTag.tag_name in list_tag:
            list_tag.append(str(mTag.tag_name))

        if not mTag.tag_name in list_tag:
            continue

        # Create file with tag name
        file_name = os.path.abspath(WS.dir_ws_analysis_events + '/' + str(mTag.tag_name))
        if not file_name in list_tag_files:
            list_tag_files.append(file_name)

        if not WriteToFile(file_name,line):
            continue

    f_buf.close()
    return list_tag_files
