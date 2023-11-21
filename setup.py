import sys
import subprocess
import setuptools
from setuptools.command.build_ext import build_ext

class Build(build_ext):
    def run(self):
        print("build libimgsmlr.so ...")
        import os
        CFLAGS = os.environ.get("CFLAGS")
        LDFLAGS = os.environ.get("LDFLAGS")
        protoc_command = ["gcc", "-g", "-Werror", "-fPIC"]
        if CFLAGS:
            protoc_command.append(CFLAGS)
        if LDFLAGS:
            protoc_command.append(LDFLAGS)
        protoc_command.extend(["-lgd", "-I", "libimgsmlr", "libimgsmlr/imgsmlr.c", "-shared",  "-o", "libimgsmlr/libimgsmlr.so"])
        print("build command: %s" % " ".join(protoc_command))
        if subprocess.call(protoc_command) != 0:
            print("build libimgsmlr.so failed!")
            sys.exit(-1)
        build_ext.run(self)

with open("pypi_readme.rst", "r") as fh:
  long_description = fh.read()
# long_description = "Implement the feature extraction function of the `imgsmlr` extension"

setuptools.setup(
    name="libimgsmlr",
    version="0.1.4",
    author="jie123108",
    author_email="jie123108@163.com",
    description="Implement the feature extraction function of the ``imgsmlr`` extension for ``PostgreSQL``.",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/jie123108/libimgsmlr",
    packages=['libimgsmlr'],
    # py_modules=['libimgsmlr'],
    keywords=['imgsmlr', 'postgres', 'image similarity search'],
    cmdclass={
        'build_ext': Build,
    },
    install_requires=["filetype"],
    package_data={'libimgsmlr': ["*.so", "Makefile", "imgsmlr.h", "imgsmlr.c"]},
)