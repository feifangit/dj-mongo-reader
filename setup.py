import os
from setuptools import setup
from djmongoreader import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='dj-mongo-reader',
    version=__version__,
    packages=['djmongoreader'],
    include_package_data=True,
    license='GPL v2.0',
    description='A Django app can be used to query and render MongoDB data',
    long_description=README,
    url='https://github.com/feifangit/dj-mongo-reader/',
    author='Fan Fei, Neil Chen',
    author_email='feifan.pub@gmail.com,neil.chen.nj@gmail.com',
    install_requires=['pymongo',],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Database',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Database :: Front-Ends',

    ],
)
