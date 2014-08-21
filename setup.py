from setuptools import setup, find_packages

setup(
    name='vman',
    version='0.0.1',
    packages=find_packages(),
    author='Dunrong Huang',
    author_email='riegamaths@gmail.com',
    description='a command line for managerment kvm virtual machine',
    license='GPLv3',
    keywords='qemu kvm virtual managerment',
    url='https://github.com/mathslinux/vman',
    entry_points={
        'command': [
            'new = new:make',
            'edit = edit:make',
            'rm = rm:make',
            'dev-add = dev:make',
            'list = list:make',
            'show = show:make',
            'up = commands:make_up',
            'down = commands:make_down',
        ],
    }
)
