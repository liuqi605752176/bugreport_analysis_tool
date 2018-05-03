import sys
"""
- Get print all adb command 
"""


cmd_dict = {}
cmd_dict['Enable diag port'] = 'adb shell setprop persist.sys.usb.config diag,serial_smd,serial_tty,rmnet_ipa,mass_storage,adb'
cmd_dict['Enable ota daemon'] = 'adb shell setprop persist.vendor.radio.start_ota_daemon 1'

def get_max_key_len(dict):
    maxLen = 0
    for key in dict:
        key_value_len = len(key)
        if key_value_len > maxLen:
            maxLen = key_value_len
    return maxLen

def display_cmd():
    maxLen = get_max_key_len(cmd_dict)
    for key in cmd_dict:
        print key + ' ' * (maxLen - len(key) + 5 ) +  ' ' + cmd_dict[key]


def main():
    display_cmd()

if __name__ == '__main__':
    main()
