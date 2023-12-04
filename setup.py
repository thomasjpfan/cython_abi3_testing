from setuptools import setup, Extension
import Cython.Build
from wheel.bdist_wheel import bdist_wheel


class bdist_wheel_abi3(bdist_wheel):
    def get_tag(self):
        python, abi, plat = super().get_tag()

        if python.startswith("cp"):
            # on CPython, our wheels are abi3 and compatible back to 3.7
            return "cp37", "abi3", plat

        return python, abi, plat


setup(
    ext_modules=[
        Extension(
            "adder.add",
            ["adder/add.pyx"],
            py_limited_api=True,
            define_macros=[
                ("Py_LIMITED_API", "0x030700f0"),
                ("CYTHON_LIMITED_API", "1"),
            ],
        )
    ],
    cmdclass={"build_ext": Cython.Build.build_ext, "bdist_wheel": bdist_wheel_abi3},
)
