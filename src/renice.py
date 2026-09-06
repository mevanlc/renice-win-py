#!/usr/bin/env python

# Copyright (c) 2019, Giampaolo Rodola', Michael Clark. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. 
# https://github.com/giampaolo/psutil/blob/master/LICENSE

echo hi

"""
In liu of a 'renice' cmdline utility on Windows.
$ winrenice chrome.exe below
13912   chrome.exe      Priority.BELOW_NORMAL_PRIORITY_CLASS
14920   chrome.exe      Priority.BELOW_NORMAL_PRIORITY_CLASS
"""

from __future__ import print_function
import sys, os, collections
import psutil

if os.name != 'nt':
    sys.exit("Platform not supported (Windows only).\nHint: Use built-in 'renice' on Linux/Unix/macOS/BSD.")

ACCESS_DENIED = ''
def renice(pgname, priority):
    procs = []
    for proc in psutil.process_iter(attrs=['name', 'cmdline']):
        # search for matches in the process name and cmdline
        if proc.info['name'] == pgname or proc.info['cmdline'] and proc.info['cmdline'][0] == pgname:
            procs.append(proc)
            proc.nice(priority)
            nproc = psutil.Process(proc.pid)
            ninfo = nproc.as_dict(attrs=['nice'], ad_value=ACCESS_DENIED)
            print("%s\t%s\t%s" % (proc.pid, proc.info['name'], ninfo['nice']))
    if len(procs) == 0:
        print("No matching processes found.")

def main():
    priority_map = collections.OrderedDict([
        ("real", psutil.REALTIME_PRIORITY_CLASS),
        ("high", psutil.HIGH_PRIORITY_CLASS),
        ("above", psutil.ABOVE_NORMAL_PRIORITY_CLASS),
        ("normal", psutil.NORMAL_PRIORITY_CLASS),
        ("below", psutil.BELOW_NORMAL_PRIORITY_CLASS),
        ("idle", psutil.IDLE_PRIORITY_CLASS),
    ])
    usage = 'usage: %s <pgname> %s' % (os.path.basename(__file__), '|'.join(priority_map.keys()))
    if len(sys.argv) != 3:
        sys.exit(usage)
    else:
        pgname = sys.argv[1]
        priarg = sys.argv[2]
    if not priarg in priority_map:
        sys.exit('Invalid priority specified.\n' + usage)
    priority = priority_map[priarg]
    renice(pgname, priority)

if __name__ == '__main__':
    main()
