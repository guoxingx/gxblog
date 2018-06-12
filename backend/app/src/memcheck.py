"""
basic memory check functions.
"""

import subprocess


def get_memory_info():
    """
    All messages from /proc/meminfo
    """
    try:
        proc = subprocess.Popen('cat /proc/meminfo', stdout=subprocess.PIPE)
        return load_data(proc.stdout)
    except FileNotFoundError:
        raise FileExistsError("os system not support")


def load_data(data):
    """
    @param: data: <io.BufferedReader> or any iterable object with content in lines.
    """
    def load_line(content):
        key, value = content.split(":")
        key, value = key.strip(), value.strip()
        return key, value
    return dict(map(load_line, data))


def memory_usage(swap=True):
    """
    Basic memory usage info.

    @params: swap: <bool> include swap memory info.
    """
    keys = ["MemTotal", "MemFree", "Buffers", "Cached"]
    data = get_memory_info()
    resp = dict(map(lambda x: (x, data.pop(x)), keys))

    memtotal = resp[keys[0]]
    memuse = sum([resp[key] for key in keys[1:]])
    resp['used'] = int(memuse * 100 / memtotal)

    return resp


if __name__ == "__main__":
    print(memory_usage())
