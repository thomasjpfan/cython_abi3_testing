from setuptools import setup, Extension
import Cython.Build

setup(
    ext_modules=[
        Extension(
            "adder.add",
            ["adder/add.pyx"],
            py_limited_api=True,
            extra_compile_args=[
                "-DCYTHON_LIMITED_API=1",
                "-DPy_LIMITED_API=0x030700f0",
            ],
        )
    ],
    cmdclass={"build_ext": Cython.Build.build_ext},
)
