import logging
from ConfigParser import ConfigParser

LOG = logging.getLogger(__name__)
vman_config = 'vman.cfg'


def new(args):
    LOG.info('Create new VM with: %s', args)

    # Create VM config
    vm_cfg = args.name + '.conf'
    parser = ConfigParser()
    parser.add_section('cpu')
    parser.set('cpu', 'number', args.cpu)
    parser.add_section('memory')
    parser.set('memory', 'size', args.memory)

    # setting VM's disk
    i = 0
    for entry in args.disk.split(','):
        disk = 'disk.%d' % (i)
        parser.add_section(disk)
        parser.set(disk, 'file', entry)
        # Now, only qcow2 format is supported
        parser.set(disk, 'format', 'qcow2')
        parser.set(disk, 'index', str(i + 1))
        i += 1

    if args.cdrom:
        parser.add_section('cdrom')
        parser.set('cdrom', 'file', args.cdrom)

    # setting VM's disk
    i = 0
    for entry in args.net.split(','):
        net = 'net.%d' % (i)
        parser.add_section(net)
        parser.set(net, 'mac', entry)
        parser.set(net, 'index', str(i + 1))
        i += 1

    # Display type
    parser.add_section('display')
    parser.set('display', 'type', args.display.split(':')[0])
    parser.set('display', 'port', args.display.split(':')[1])

    # Bootorder
    parser.add_section('bootorder')
    parser.set('bootorder', 'type', args.bootorder)

    # Write all setting to config file
    parser.write(open(vm_cfg, 'w'))

    # Create a new entry into our vman config file to announce our VM
    # TODO: need a config dir?
    parser = ConfigParser()
    parser.read(vman_config)
    parser.add_section(args.name)
    parser.set(args.name, 'config', vm_cfg)
    parser.write(open(vman_config, 'w'))

def make(parser):
    """
    Create a new virtual machine
    """
    parser.add_argument(
        'name',
        help='name of this VM'
    )
    parser.add_argument(
        '--cpu',
        metavar='CPUNumber',
        default=2,
        type=int,
        help='cpu number of this VM'
    )
    parser.add_argument(
        '--memory',
        metavar='MemorySize',
        default=1024,
        type=int,
        help='memory size of this VM'
    )
    parser.add_argument(
        '--disk',
        metavar='Disk',
        required=True,
        help='Disk of this VM'
    )
    parser.add_argument(
        '--cdrom',
        metavar='CPUNumber',
        help='Cdrom of this VM'
    )
    parser.add_argument(
        '--net',
        metavar='MacAddress',
        required=True,
        help='Mac address of this VM'
    )
    parser.add_argument(
        '--display',
        metavar='Display type',
        required=True,
        help='Display type of this VM'
    )
    parser.add_argument(
        '--bootorder',
        metavar='BootOrder',
        choices=[
            'disk',
            'cdrom',
        ],
        default='disk',
        help='Boot order of this VM'
    )

    parser.set_defaults(func=new)
