from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    readme = f.read()

setup(
    name='requests_o365',
    version='0.1',
    description='Office 365 wrapper for reuqests_oauthlib',
    long_description=readme,
    url='http://github.com/mwallace/requests_o365',
    author='Matt Wallace',
    author_email='matthew.r.wallace@live.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    packages=['requests_o365'],
    zip_safe=False
)
