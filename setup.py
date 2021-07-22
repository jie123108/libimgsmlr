import sys
import subprocess
import setuptools
from setuptools.command.build_ext import build_ext

class Build(build_ext):
    def run(self):
        print("build libimgsmlr.so ...")
        protoc_command = ["gcc", "-g", "-Werror", "-fPIC", "-lgd", "libimgsmlr/imgsmlr.c", "-shared",  "-o", "libimgsmlr/libimgsmlr.so"]
        if subprocess.call(protoc_command) != 0:
            print("build libimgsmlr.so failed!")
            sys.exit(-1)
        build_ext.run(self)

with open("pypi_readme.rst", "r") as fh:
  long_description = fh.read()
# long_description = "Implement the feature extraction function of the `imgsmlr` plugin"

setuptools.setup(
    name="libimgsmlr",
    version="0.0.7",
    author="jie123108",
    author_email="jie123108@163.com",
    description="Implement the feature extraction function of the ``imgsmlr`` plugin for ``PostgreSQL``.",
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
    package_data={'libimgsmlr': ["*.so", "Makefile", "imgsmlr.c"]},
)