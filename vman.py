#!/usr/bin/python

"""
vman add vm1.conf
vman up vm1
vman info vm1
vman ssh vm1
vman down vm1
vman remove vm1
"""

import sys
import traceback
from commands import run_command

def main(args):
    if len(sys.argv) < 2:
        print "Usage: \n  vman <command> [options]"
        sys.exit(1)

    try:
        run_command(args[0], args)
    except:
        traceback.print_exc()

if __name__ == '__main__':
    main(sys.argv[1:])
