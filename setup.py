import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.txt')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

install_requires=[]
test_requires = ['zope.testing']

__version__ = "0.1"

setup(name='svgsize',
      version=__version__,
      description='A simple library that reads size (dimensions) from a SVG image',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: BSD-Like",
      ],
      url="http://github.com/avnik/svgsize/",
      author="Alexander V. Nikolaev",
      
      license="BSD-derived",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      namespace_packages = ['svgsize'],
      install_requires = install_requires,
      tests_require= test_requires,
      extras_require = {
          'test': test_requires,
      },
)

