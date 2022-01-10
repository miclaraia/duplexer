from setuptools import setup
import os

def load_version():
    here = os.path.abspath(os.path.dirname(__file__))
    versionfile = os.path.join(here, 'VERSION')
    with open(versionfile, 'r') as f:
        versionstring = f.readline().strip()

    return versionstring

setup(
    name='duplexer',
    version=load_version(),
    packages=['duplexer'],
    install_requires=[
        'pycups',
        'ghostscript',
        'PyPDF2'
    ],
    entry_points={
    'console_scripts': [
        'duplexer=duplexer.main:main',
    ],
},

)
