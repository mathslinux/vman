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
import logging
import excp
import argparse
import pkg_resources

LOG = logging.getLogger(__name__)


def set_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(name)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def create_parser():
    parser = argparse.ArgumentParser(
        prog='guest-tools',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Convenient tools for qemu guest image\n\n',
        )
    sub = parser.add_subparsers(
        title='Commands',
        metavar='COMMAND',
        help='description',
        )
    entry_points = [
        (e.name, e.load()) for e in pkg_resources.iter_entry_points('command')
    ]
    for (name, fn) in entry_points:
        p = sub.add_parser(
            name,
            description=fn.__doc__,
            help=fn.__doc__,
        )
        fn(p)
    return parser


@excp.catches((KeyboardInterrupt, RuntimeError, excp.VmanError,))
def main(args):
    parser = create_parser()
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit()
    else:
        args = parser.parse_args()

    set_logger()

    return args.func(args)

if __name__ == '__main__':
    sys.exit(main())
