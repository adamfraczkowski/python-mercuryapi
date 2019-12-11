# python3 setup.py build
# python3 setup.py sdist upload
from setuptools import setup, Extension
from distutils.command.build import build
import os, platform, sys

# PATH DEPENDS ONLY ON YOUR BUILD ENV
STAGING_DIR="/root/source/staging_dir"
TOOLCHAIN_DIR=STAGING_DIR+"/toolchain-mipsel_24kc_gcc-7.3.0_musl"
CC=TOOLCHAIN_DIR+"/bin/mipsel-openwrt-linux-gcc"
STRIP=TOOLCHAIN_DIR+"/bin/mipsel-openwrt-linux-strip"
LDSHARED=TOOLCHAIN_DIR+"/bin/mipsel-openwrt-linux-gcc -shared"
PYTHONXCPREFIX=STAGING_DIR+"/target-mipsel_24kc_musl/usr"
LDFLAGS="-L"+STAGING_DIR+"/target-mipsel_24kc_musl/usr/lib "+"-L"+STAGING_DIR+"/target-mipsel_24kc_musl/lib"

os.environ['STAGING_DIR'] = STAGING_DIR;
os.environ['TOOLCHAIN_DIR'] = TOOLCHAIN_DIR;
os.environ['CC'] = CC;
os.environ['LDSHARED'] = LDSHARED
os.environ['PYTHONXCPREFIX'] = PYTHONXCPREFIX
os.environ['LDFLAGS'] = LDFLAGS


class my_build(build):
    def run(self):
        if platform.system() == 'Darwin':
            os.system("cp -f mercuryapi_osx.patch mercuryapi.patch")
        os.system("make mercuryapi")
        build.run(self)

setup(name="python-mercuryapi", version="0.5.3",
      author="Petr Gotthard",
      author_email="petr.gotthard@centrum.cz",
      description="Python wrapper for the ThingMagic Mercury API",
      long_description=open('long_description.txt').read(),
      url="https://github.com/gotthardp/python-mercuryapi",
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