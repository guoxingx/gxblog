"""
basic memory check functions.
"""

import subprocess


def get_memory_info(remote_addr=None):
    """
    All messages from /proc/meminfo

    @param: remote_addr: <str>: use remote addr with string - "username@ip:port"
    """
    try:
        cmd = 'cat /proc/meminfo'
        if remote_addr:
            cmd = ssh_remote(remote_addr, cmd)
        proc = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, shell=False)
        return load_data(proc.stdout)
    except FileNotFoundError:
        raise FileExistsError("os system not support")


def load_data(data):
    """
    @param: data: <io.BufferedReader> or any iterable object with content in lines.
    """
    def load_line(content):
        key, value = content.decode().split(":")
        key, value = key.strip(), value.strip()
        return key, value
    return dict(map(load_line, data))


def get_used_memory(swap=True, remote_addr=None):
    """
    Basic memory usage info.

    @param: swap: <bool> include swap memory info.
    @param: remote_addr: <str>: use remote addr with string - "username@ip:port"
    """
    keys = ["MemTotal", "MemFree", "Buffers", "Cached"]
    data = get_memory_info(remote_addr)
    resp = dict(map(lambda x: (x, data.pop(x)), keys))

    memtotal = get_integer_value(resp, keys[0])
    memfree = get_integer_value(resp, keys[1])
    if memtotal and memfree:
        resp['used'] = int(100 - memfree * 100 / memtotal)
    return resp


def ssh_remote(remote_addr, cmd):
    """
    return executable cmd with ssh ... and given command

    @param: remote_addr: <str>: use remote addr with string - "username@ip:port"
    @param: cmd: <str>: cmd to run.
    """
    username, remote_addr = remote_addr.split('@')
    ip, port = remote_addr.split(':')
    return 'ssh {}@{} -p {} {}'.format(username, ip, port, cmd)


def get_integer_value(info, key):
    value_string = info.get(key)
    if not value_string:
        return None
    try:
        value = int(value_string.strip().split(" ")[0])
    except ValueError as e:
        print("unable to get integer value from ", value_string)
        value = None
    finally:
        return value


if __name__ == "__main__":
    REMOTE = 'root@95.163.201.173:29744'
    print(get_used_memory(remote_addr=REMOTE))
