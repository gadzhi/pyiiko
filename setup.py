from setuptools import setup, find_packages
from os.path import join, dirname


setup(
    name='Pyiiko',
    description='Library for iikoAPI',
    url='https://github.com/gadzhi/pyiiko',
    author='Gadzhibala Pirmagomedov',
    author_email='gadzhibala@protonmail.com',
    version='0.2.12',
    packages=find_packages(),
    include_package_data=True,
    test_suite='tests',
    install_requires=[
        'requests>=2.20.0',
        'lxml>=4.1.1'

    ]
)
