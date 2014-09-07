import libvirt


class VMManager(object):
    """
    """

    def __init__(self):
        """
        """

    def up(self, xml):
        conn = libvirt.open('qemu:///system')
        conn.createXML(xml, 0)
        conn.close()

    def list_vm_names(self):
        """Get all vm names managered by libvirt
        """
        conn = libvirt.open('qemu:///system')
        dms = []
        for dm in conn.listAllDomains():
            dms.append(dm.name())
        conn.close()
        return dms

    def down(self, name):
        conn = libvirt.open('qemu:///system')
        try:
            domain = conn.lookupByName(name)
            domain.destroyFlags(libvirt.VIR_DOMAIN_DESTROY_GRACEFUL)
        except:
            print "No VM named %s" % name
        conn.close()
