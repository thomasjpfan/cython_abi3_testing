from setuptools import setup, Extension
from Cython.Build import build_ext as cython_build_ext
from wheel.bdist_wheel import bdist_wheel
from setuptools.command.build_ext import get_abi3_suffix, get_config_var

PY_LIMITED_API = "0x030600f0"
MIN_PYTHON_VERSION = "3.6"
CPYTHON_TAG = f"cp{MIN_PYTHON_VERSION.replace('.', '')}"

extensions = [
    Extension(
        "adder.add",
        sources=["adder/add.pyx"],
        py_limited_api=True,
        define_macros=[
            ("Py_LIMITED_API", "0x030600f0"),
            ("CYTHON_LIMITED_API", "1"),
        ],
    )
]


class bdist_wheel_abi3(bdist_wheel):
    def get_tag(self):
        python, abi, plat = super().get_tag()

        if python.startswith("cp"):
            return CPYTHON_TAG, "abi3", plat

        return python, abi, plat


class bdist_ext_abi3(cython_build_ext):
    def get_ext_filename(self, fullname):
        filename = super().get_ext_filename(fullname)
        if fullname in self.ext_map:
            ext = self.ext_map[fullname]
            use_abi3 = getattr(ext, "py_limited_api") and get_abi3_suffix()
            if use_abi3:
                so_ext = get_config_var("EXT_SUFFIX")
                filename = filename[: -len(so_ext)]
                filename = filename + get_abi3_suffix()
        return filename

    def initialize_options(self):
        super().initialize_options()
        self.ext_map = {}

    def finalize_options(self):
        super().finalize_options()
        for ext in self.extensions:
            fullname = self.get_ext_fullname(ext.name)
            self.ext_map[fullname] = ext
            self.ext_map[fullname.split(".")[-1]] = ext


setup(
    name="adder",
    packages=["adder"],
    ext_modules=extensions,
    python_requires=f">={MIN_PYTHON_VERSION}",
    cmdclass={"build_ext": bdist_ext_abi3, "bdist_wheel": bdist_wheel_abi3},
)
