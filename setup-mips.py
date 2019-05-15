# python3 setup.py build
# python3 setup.py sdist upload
from setuptools import setup, Extension
from distutils.command.build import build
import os

class my_build(build):
    def run(self):
        os.system("make mercuryapi")
        build.run(self)

setup(name="python-mercuryapi", version="0.4.2",
      author="Adam Fraczkowski",
      author_email="adam.fraczkowski@gmail.com",
      description="Python wrapper for the ThingMagic Mercury API for OpenWRT",
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      url="https://github.com/adamfraczkowski/python-mercuryapi",
      classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta"
      ],
      cmdclass={'build': my_build},
      ext_modules=[Extension("mercury",
                             sources=["mercury.c"],
                             libraries=["mercuryapi", "ltkc", "ltkctm"],
                             include_dirs=['build/mercuryapi/include'],
                             library_dirs=['build/mercuryapi/lib'])])
