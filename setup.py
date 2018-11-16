
from setuptools import setup, find_packages
from codecs import open
from os import path
import tsunami

here = path.abspath(path.dirname(__file__))


setup(
    name='tsunamiweb',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=tsunami.VERSION,

    description='tsunami.',
    long_description='',

    # The project's main homepage.
    url='',

    # Author details
    author='Jerevia',
    author_email='trilliondawn@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],

    # What does your project relate to?
    keywords='tsunami aiohttp webframework web framework asyncio uvloop',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    include_package_data=True,

    install_requires=[
        'aiohttp',
        'pytest-aiohttp',
        'uvloop',
        'gunicorn'
    ],

    python_requires='>=3.6',

    extras_require={
        'dev': [],
        'test': [],
    },

    entry_points={
        'console_scripts': [
            'tsunami = tsunami.core.management:execute_from_command_line',
        ],
    },
)