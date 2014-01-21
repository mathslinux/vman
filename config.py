from ConfigParser import ConfigParser, NoOptionError, NoSectionError
from excp import ConfigError
import xml.etree.cElementTree as ET
import glob

vman_config = '/tmp/vman.conf'


class VmanConfig(object):
    """Config file for general config, i.e. manager file "vman_config"
    """

    def get_vm_config(self, name):
        p = ConfigParser()
        p.read(vman_config)
        return p.get(name, 'config')


class VMConfig(object):
    """Config file for Virtual Machine
    """

    def __init__(self, name):
        self.name = name
        c = VmanConfig()
        self.config = c.get_vm_config(name)

    def _parse_general(self, parser, domain):
        os_tag = ET.SubElement(domain, 'os')
        os_type = ET.SubElement(os_tag, 'type', arch='x86_64')
        os_type.text = 'hvm'
        vm_name = ET.SubElement(domain, 'name')
        vm_name.text = self.name

    def _parse_cpu(self, parser, domain):
        cpu_num = parser.get('cpu', 'number')
        if cpu_num > 0:
            cpu = ET.SubElement(domain, 'vcpu')
            cpu.text = cpu_num

    def _parse_memory(self, parser, domain):
        # The size unit is M(1024KB)
        mem_size = parser.get('memory', 'size')
        mem = ET.SubElement(domain, 'memory')
        if mem_size > 0:
            mem.text = str(int(mem_size) * 1024)
        else:
            mem.text = str(512 * 1024)

    def _parse_device_section(self, parser, name, entries):
        """
        Parse device section, e.g, net, disk, and return a list like:
        [{'index': '1', 'file': 'vm1.qcow2', 'format': 'qcow2'},
         {'index':2, 'file': 'disk.qcow2', 'format': 'qcow2'}]
        """
        device_list = []
        for section in parser.sections():
            if section.startswith(name):
                device = dict()
                for e in entries:
                    try:
                        value = parser.get(section, e)
                        device[e] = value
                    except NoOptionError:
                        pass
                if device:
                    device_list.append(device)

        if not device_list:
            raise ConfigError('no %s config!' % (name))

        # If there is only a device of this type in config file and index is
        # not defined, we set the value of index to 1 by default
        if len(device_list) == 1:
            device = device_list[0]
            if 'index' not in device.keys():
                device['index'] = '1'

        # Check whether all config needed by device have been defined
        for device in device_list:
            if not set(entries).issubset(device.keys()):
                raise ConfigError('Please provide more details for %s '
                                  'device' % (name))

        return device_list

    def _parse_disk(self, parser, domain):
        """
        - parse disk section
        """

        devices = domain.find('devices')
        for disk in self._parse_device_section(parser, 'disk',
                                               ['file', 'format', 'index']):
            node = ET.SubElement(devices, 'disk', type='file', device='disk')

            index = int(disk['index'])
            dev = 'vd' + chr(ord('a') + index - 1)  # vda, vdb, vdc ...
            slot = str(hex(6 + index - 1))          # PCI address:0x6, 0x7, 0x8

            ET.SubElement(node, 'boot', order=disk['index'])
            ET.SubElement(node, 'source', file=disk['file'])
            ET.SubElement(node, 'target', bus='virtio', dev=dev)
            ET.SubElement(node, 'address', type='pci', bus='0x00',
                          slot=slot, function='0x0')
            ET.SubElement(node, 'driver', type=disk['format'], name='qemu')

    def _parse_net(self, parser, domain):
        """
        Create xml for a net device.

        <interface type="bridge">
          <address  domain="0x0000"  function="0x0"  slot="0x03"  type="pci" bus="0x00"/>
          <mac address="00:1a:4a:a8:00:77"/>
          <model type="e1000"/>
          <source bridge="ctmgmt"/>
          </interface>
        """
        self._parse_device_section(parser, 'net', ['mac', 'index'])
        devices = domain.find('devices')
        bridges = [b.split('/')[-2] for b in glob.glob('/sys/class/net/*/bridge')]
        net_list = self._parse_device_section(parser, 'net', ['mac', 'index'])
        # TODO: NAT support, index limitation
        if bridges:
            for net in net_list:
                index = int(net['index'])
                slot = str(hex(3 + index - 1))  # PCI address:0x6, 0x7, 0x8
                node = ET.SubElement(devices, 'interface', type='bridge')

                ET.SubElement(node, 'address', function='0x0', slot=slot,
                              type='pci', bus='0x00')
                ET.SubElement(node, 'mac', address=net['mac'])
                ET.SubElement(node, 'model', type='virtio')
                ET.SubElement(node, 'source', bridge=bridges[0])

    def _parse_display(self, parser, domain):
        devices = domain.find('devices')
        try:
            d_type = parser.get('display', 'type')
            d_port = parser.get('display', 'port')

            display = ET.SubElement(devices, 'graphics', type=d_type, port=d_port,
                                autoport='no')
            ET.SubElement(display, 'listen', type='address', address='0.0.0.0')
        except NoSectionError:
            # Allow to define a VM which has no display device
            pass

    def toxml(self):
        """Convert our config file to xml string libvirt needs to manager VM
        """
        p = ConfigParser()
        p.read(self.config)

        domain = ET.Element('domain', type='kvm')

        self._parse_general(p, domain)
        self._parse_cpu(p, domain)
        self._parse_memory(p, domain)

        # Create device config
        ET.SubElement(domain, 'devices')
        self._parse_disk(p, domain)
        self._parse_net(p, domain)
        self._parse_display(p, domain)

        return ET.tostring(domain)
