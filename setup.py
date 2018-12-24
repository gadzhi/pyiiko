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
    include_package_data=True,
    test_suite='tests',
    install_requires=[
        'requests>=2.20.0',
        'pytest>= 3.4.2',
        'lxml>=4.1.1'

    ]
)
