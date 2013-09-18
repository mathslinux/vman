from ConfigParser import ConfigParser, NoOptionError
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
        os_type = ET.SubElement(os_tag, 'type', arch='x86_64', machine='pc')
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

    def _parse_disk_section(self, parser):
        """
        Parse disk section and return a list like:
        [{'index': '1', 'file': 'vm1.qcow2', 'format': 'qcow2'},
         {'index':1, 'file': 'disk.qcow2', 'format': 'qcow2'}]
        """
        disk_list = []
        entrys = ['file', 'format', 'index']
        for section in parser.sections():
            if section.startswith('disk'):
                disk = dict()
                for e in entrys:
                    try:
                        value = parser.get(section, e)
                        disk[e] = value
                    except NoOptionError:
                        pass
                if disk:
                    disk_list.append(disk)

        if not disk_list:
            raise ConfigError('no disk config!')

        # If there is only a disk in config file and index is not defined,
        # we set the value of index to 1 by default
        if len(disk_list) == 1:
            disk = disk_list[0]
            if 'index' not in disk.keys():
                disk['index'] = '1'

        # Check whether all config needed by disk have been defined
        for disk in disk_list:
            if not set(entrys).issubset(disk.keys()):
                raise ConfigError('file or format or index are not defined!')

        return disk_list

    def _parse_disk(self, parser, domain):
        """
        - parse disk section
        """

        devices = domain.find('devices')
        for disk in self._parse_disk_section(parser):
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
        devices = domain.find('devices')
        mac = parser.get('net', 'mac')
        bridges = [b.split('/')[-2] for b in glob.glob('/sys/class/net/*/bridge')]
        if bridges:
            # FIXME: dont hard code
            iface = ET.SubElement(devices, 'interface', type='bridge')
            ET.SubElement(iface, 'address', domain='0x0000', function='0x0',
                          slot='0x3', type='pci', bus='0x00')
            ET.SubElement(iface, 'mac', address=mac)
            ET.SubElement(iface, 'model', type='virtio')
            ET.SubElement(iface, 'source', bridge=bridges[0])

    def _parse_display(self, parser, domain):
        devices = domain.find('devices')
        d_type = parser.get('display', 'type')
        d_port = parser.get('display', 'port')

        display = ET.SubElement(devices, 'graphics', type=d_type, port=d_port,
                                autoport='no')
        ET.SubElement(display, 'listen', type='address', address='0.0.0.0')

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
