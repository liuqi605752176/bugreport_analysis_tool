import subprocess
import os


def run_shell_command(cmd):
    cmd_list = cmd.split()
    try:
        cmd_stdout = subprocess.Popen(
            cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError as err:
        print 'failed to excute comannd - error: ', err
        print 'command : ' + cmd
        return False, False
    if not cmd_stdout:
        print 'command return null '
        return False, False

    out_buf = cmd_stdout.stdout

    # print '-' * 90
    # print out_buf
    # for line in out_buf:
    #     print line,
    # print '-' * 90

    return out_buf, True


def cmd(cmd_str):
    adb_prefix = 'adb '
    command = adb_prefix + cmd_str
    out_buf, is_ok = run_shell_command(command)

    if not is_ok:
        print 'failed to get data from command'
        return False

    data_in_list = []
    for line in out_buf:
        data_in_list.append(line)

    # print data_in_list
    return data_in_list

# return a list of data
def shell_command(cmd_str):
    shell_perfix = 'shell '
    command = shell_perfix + cmd_str
    return cmd(command)


def wait_for_adb():
    cmd('wait-for-device')


def is_device_online():
    data_list = cmd('devices')
    out = data_list[1]
    print ' out : ' + out
    if out == '\n':
        print 'adb device not connected'
        return False

    return data_list[1]


# def check_adb():
#     run_shell_command('adb devices')
