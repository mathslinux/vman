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
    except Exception as detail:
        print traceback.print_exc()
        return

if __name__ == '__main__':
    main(sys.argv[1:])
