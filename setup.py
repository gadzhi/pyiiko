from setuptools import setup, find_packages
from os.path import join, dirname
import Pyiiko

setup(
    name='Pyiiko',
    description='Library for iikoAPI',
    url='https://github.com/gadzhi/pyiiko',
    author='Gadzhibala Pirmagomedov',
    author_email='gadzhibala@protonmail.com',
    version=Pyiiko.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    include_package_data=True,
    test_suite='tests',
    install_requires=[
        'requests==2.18.4'
    ]
)
