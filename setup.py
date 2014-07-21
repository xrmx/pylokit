from setuptools import setup, find_packages
import os

VERSION = "0.8.0"

CLASSIFIERS = [
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Office/Business :: Office Suites',
]

setup(
    author="Riccardo Magliocchetti",
    author_email="riccardo.magliocchetti@gmail.com",
    name='pylokit',
    version=VERSION,
    description='Python CFFI wrapper for LibreOfficeKit',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url="https://github.com/xrmx/pylokit",
    license='MPL 2.0',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'cffi',
        'six',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe = False,
)
