import libvirt


class VMManager(object):
    """
    """

    def __init__(self):
        """
        """

    def up(self, xml):
        conn = libvirt.open('qemu:///system')
        print xml
        conn.createXML(xml)
        conn.close()

    def down(self, name):
        conn = libvirt.open('qemu:///system')
        try:
            domain = conn.lookupByName(name)
            domain.destroyFlags(libvirt.VIR_DOMAIN_DESTROY_GRACEFUL)
        except:
            print "No VM named %s" % name
        conn.close()
