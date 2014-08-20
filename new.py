def new(args):
    print args


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
        choices=[
            'vnc',
            'spice',
        ],
        default='vnc',
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
