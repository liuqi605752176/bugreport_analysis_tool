"""event_classess.py module has all required class definition
for event analyzer
"""

class Tag(object):
    """Tag class represent event log tag information
    """
    def __init__(self):
        self.date = None
        self.time = None
        self.log_uid = None
        self.log_pid = None
        self.log_tid = None
        self.log_level = None
        self.tag_name = None

class EventAmProc(object):
    """EventAmProc class represent am_proc_xxxx tag information
    """
    def __init__(self):
        self.tag = Tag()
        self.user = None
        self.pid = None
        self.name = None
        self.p_type = None
        self.component = None
