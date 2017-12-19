#! /usr/bin/env python

import os
import stat
import sys

def get_all_locks():
    FILE = open('/proc/locks')
    locks = {}
    for f in FILE.readlines():
        line = f.split()
        pid = line[4]
        inode = line[5].split(':')
        inode = int(inode[2])
        if inode in locks:
            locks[inode] += [pid]
        else:
            locks[inode] = [pid]
    return locks

def get_file_inodes(lockdir):
    entries = os.listdir(lockdir)
    files = {}
    for e in entries:
        path = lockdir.rstrip('/') + '/' + e
        attrs = os.stat(path)
        if stat.S_ISREG(attrs.st_mode):
            files[attrs.st_ino] = path
    return files

if len(sys.argv) != 2:
    sys.exit(1)
lockdir = sys.argv[1]
files = get_file_inodes(lockdir)
locks = get_all_locks()
for k in files.keys():
    if locks.has_key(k):
        print locks[k], files[k]
