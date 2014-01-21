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
import logging
from commands import run_command
import excp

LOG = logging.getLogger(__name__)


def set_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(name)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


@excp.catches((KeyboardInterrupt, RuntimeError, excp.VmanError,))
def main(args):
    if len(sys.argv) < 2:
        print "Usage: \n  vman <command> [options]"
        sys.exit(1)

    set_logger()

    try:
        run_command(args[0], args)
    except:
        traceback.print_exc()

if __name__ == '__main__':
    main(sys.argv[1:])
