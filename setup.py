from setuptools import setup, find_packages, Extension

setup(
    name = 'stormed',
    version = '0.1',
    packages = find_packages(exclude=['test*']),
    include_package_data = True,
)

