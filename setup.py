from setuptools import setup, Extension
import Cython.Build

setup(
    ext_modules=[Extension("*", ["*.pyx"])],
    cmdclass={"build_ext": Cython.Build.build_ext}
)
