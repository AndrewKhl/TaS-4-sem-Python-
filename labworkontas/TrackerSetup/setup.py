from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='WTask',
    version='1.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    entry_points={
        'console_scripts':
            ['main = tracker.main:main',
             'wtask = command_line.comline:main']
        },
    include_package_data=True,
    test_suite='tests.test_tracker'
)
