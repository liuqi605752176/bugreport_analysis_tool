
## Tag information
class Tag(object):
     def __init__(self):
        self.date = None
        self.time = None
        self.log_uid = None
        self.log_pid = None
        self.log_tid = None
        self.log_level = None
        self.tag_name = None

# 04-25 11:44:56.563  1000  1656  2987 I am_proc_died: [0,4892,com.google.android.apps.photos,906,17]
# 04-25 11:45:04.725  1000  1656  2987 I am_proc_start: [0,5716,10016,com.google.android.gms.unstable,service,com.google.android.gms/.droidguard.DroidGuardService]
# 04-25 11:45:04.748  1000  1656  2987 I am_proc_bound: [0,5716,com.google.android.gms.unstable]
## Event log
class EventAmProc(object):
    def __init__(self):
        self.tag = Tag()
        self.user = None
        self.pid = None
        self.name = None
        self.p_type = None
        self.component = None
