import os
import logging
from ConfigParser import ConfigParser

LOG = logging.getLogger(__name__)
vman_config = 'vman.cfg'


def rm(args):
    p = ConfigParser()
    vm_cfg = args.name + '.conf'
    p.read(vm_cfg)

    for section in p.sections():
        if section.startswith('disk'):
            LOG.debug('Delete VM %s', args.name)
            try:
                f = p.get(section, 'file')
                LOG.info('Delete VM disk %s', f)
                os.unlink(f)
            except OSError as e:
                raise RuntimeError(e)

    LOG.debug('Delete VM config %s', vm_cfg)
    try:
        os.unlink(vm_cfg)
    except OSError:
        LOG.warn('%s is not exist' %  vm_cfg)

    LOG.debug('Delete VM item from config file')
    p = ConfigParser()
    p.read(vman_config)
    p.remove_section(args.name)
    p.write(open(vman_config, 'w'))


def make(parser):
    """
    Delete a virtual machine
    """
    parser.add_argument(
        'name',
        help='name of this VM'
    )
    parser.set_defaults(func=rm)
