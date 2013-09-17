#!/usr/bin/python

import os
import argparse
import shutil
from ConfigParser import ConfigParser
from excp import CommandError
from manager import VMManager
from config import vman_config, VMConfig


class Help(object):
    """ Show help for commands
    """

    name = 'help'

    def __init__(self, args):
        pass

    def run(self):
        print "Usage: \n  vman <command> [options]"


class Add(object):
    """
    Add a VM instance to our managerment
    vman add vm1.conf --name vm1
    """

    name = 'add'

    def __init__(self, args):
        parser = argparse.ArgumentParser(prog='vman add', usage="vman add "
                                         "vm.conf --name NAME")
        parser.add_argument('config', nargs=1)
        parser.add_argument('--name', required=True)
        ret = parser.parse_args(args[1:])
        self.config_file = ret.config[0]
        self.vm_name = ret.name

        #FIXME: can be configured by config file
        self.vman_dir = '/tmp'

    def help(self):
        """Show help about command "add"
        """

    def run(self):
        src_file = self.config_file
        dest_file = os.path.join(self.vman_dir, os.path.basename(src_file))

        shutil.copyfile(src_file, dest_file)

        # Create a new entry into our vman config file to announce our vm
        parser = ConfigParser()
        parser.read(vman_config)

        parser.add_section(self.vm_name)
        parser.set(self.vm_name, 'config', dest_file)
        parser.write(open(vman_config, 'w'))


class UP(object):
    """ Start a VM instance
    vman up vm1
    """

    name = 'up'

    def __init__(self, args):
        """
        """
        # args of this command has only one element, like ['vm1']
        if (len(args) != 2):
            raise CommandError('Command "up" has only one argument!')

        self.vm_name = args[1]     # Save VM's name, will be used later

    def help(self):
        """Show help about command "UP"
        """

    def run(self):
        c = VMConfig(self.vm_name)
        manager = VMManager()
        manager.up(c.toxml())


class Down(object):
    """ Shutdown a VM
    vman down vm1
    """

    name = 'down'

    def __init__(self, args):
        if (len(args) != 2):
            raise CommandError('Command "down" has only one argument!')
        self.vm_name = args[1]

    def run(self):
        manager = VMManager()
        manager.down(self.vm_name)
        pass

        '''
class Info(object):
    """ Show information of instance
    """

    def __init__(self, *args, **kw):
        """
        """

    def run(self):
        pass

class SSH(object):
    """ connect to a VM instance through ssh protocol, so cool
    """

    def __init__(self, *args, **kw):
        """
        """

    def run(self):
        pass

class Remove(object):
    """ Remove a VM instance from our managerment
    """

    def __init__(self, *args, **kw):
        """
        """

    def run(self):
        pass
'''

commands = {
    Help.name: Help,
    Add.name: Add,
    UP.name: UP,
    Down.name: Down,
}
"""
    Info.name: Info,
    SSH.name: ssh,
    Down.name: Down,
    Remove.name: Remove,
"""


def run_command(name, args):
    commands[name](args).run()
