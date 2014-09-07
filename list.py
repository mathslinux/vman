from ConfigParser import ConfigParser
from manager import VMManager

vman_config = 'vman.cfg'


def get_mac(cfg):
    p = ConfigParser()
    p.read(cfg)
    mac = []
    for s in p.sections():
        if s.startswith('net'):
            mac.append(p.get(s, 'mac'))

    return mac


def list(args):
    p = ConfigParser()
    p.read(vman_config)
    vms = p.sections()
    fmt = '%-20s %-6s'
    output = ['Name', 'Status']
    if args.ip:
        fmt = fmt + ' %-16s'
        output.append('IPAddress')
    if args.mac:
        fmt = fmt + ' %-20s'
        output.append('MACAddress')
    if args.all:
        fmt = '%-20s %-6s %-16s %-20s'
        output = ['Name', 'Status', 'IPAddress', 'MACAddress']
    print fmt % tuple(output)
    print '-'*60

    dms = VMManager().list_vm_names() # all running virtual machine domain
    for v in vms:
        status = 'Down'
        if v in dms:
            status = 'Up'
        output = [v, status]
        if args.mac or args.all:
            mac = ','.join(get_mac(p.get(v, 'config')))

        if args.ip:
            output.append('to be done')
        if args.mac:
            output.append(mac)
        if args.all:
            output = [v, status, 'to be done', mac]
        print fmt % tuple(output)


def make(parser):
    """
    List the VM's information
    """
    parser.add_argument(
        '--mac',
        action='store_true',
        help='whether show MAC address or not'
    )

    parser.add_argument(
        '--ip',
        action='store_true',
        help='whether show IP address or not'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='whether show all information or not'
    )

    parser.set_defaults(func=list)
