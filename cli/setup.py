from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("sys_interface_funcs.pyx", language_level=3)
)
