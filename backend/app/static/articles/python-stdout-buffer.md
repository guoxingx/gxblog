# python stdout buffer 
nohup python do not write 'print()'

## Problem
Problem founded with running: `nohup python wsgi.py > log-wsgi.log 2>&1 < /dev/null &`, all the `print()` statements was not written into the file.

I know logging is the better way, but......

## Cause

Cased by python's buffer for output with print().

> output buffering works differently depending on if the output goes to a tty or another process/pipe. If it goes to a tty, then it is flushed after each `\n`, but in a pipe it is buffered.
https://stackoverflow.com/questions/107705/disable-output-buffering


## Solutions

### 1. python -u [pending]
As the python docs: https://docs.python.org/2/using/cmdline.html#cmdoption-u, 

force to disable buffer. which **is not work** for me in python 3.6.2, MacOs 10.12.6

### 2. warp sys.stdout [success]

unbuffer.py as:


```
import sys

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr(self, attr):
        return getattr(self.stream, attr)


def unbuffer():
    sys.stdout = Unbuffered(sys.stdout)
```

execute it in "main".

sys.__stdout__ never changed incase you need id.

### 3. print(msg, flush=True) [success]

available in Using Python 3.3 and later versions.

for the other versions:

```
from __future__ import print_function
import sys

if sys.version_info[:2] < (3, 3):
    old_print = print
    def print(*args, **kwargs):
        flush = kwargs.pop('flush', False)
        old_print(*args, **kwargs)
        if flush:
            file = kwargs.get('file', sys.stdout)
            # Why might file=None? IDK, but it works for print(i, file=None)
            file.flush() if file is not None else sys.stdout.flush()
```

But I am not quite used with `print(msg, Flush=True)`

## Links
https://stackoverflow.com/questions/12919980/nohup-is-not-writing-log-to-output-file

https://stackoverflow.com/questions/34753765/nohup-and-python-u-it-still-doesnt-log-data-in-realtime

https://stackoverflow.com/questions/107705/disable-output-buffering

https://stackoverflow.com/questions/230751/how-to-flush-output-of-python-print



