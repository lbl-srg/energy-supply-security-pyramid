import io
import platform
import os
from setuptools import setup

# Python setup file.
# See http://packages.python.org/an_example_pypi_project/setuptools.html

MAIN_PACKAGE = 'maslow'
PACKAGE_PATH =  os.path.abspath(os.path.join(os.path.dirname(__file__), MAIN_PACKAGE))

# Version.
version_path = os.path.join(PACKAGE_PATH, 'VERSION')
with open(version_path) as f:
    VERSION = f.read().strip()

# Readme.
readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'README.md'))
with io.open(readme_path, encoding='utf-8') as f:  # io.open for Python 2 support with encoding
    README = f.read()

setup(
    name=MAIN_PACKAGE,
    version=VERSION,
    author="Michael Wetter",
    author_email="mwetter@lbl.gov",
    description=(
        "Package for calculating the energy security metrics"),
    long_description=README,
    long_description_content_type='text/x-rst',
    license="3-clause BSD",
    keywords="",
    python_requires='>=3.8',
    install_requires=[
        'numpy',
        'openpyxl',
        'pandas'
    ]
)
