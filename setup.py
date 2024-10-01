import os
import warnings
from pathlib import Path

import pybind11
from setuptools import Extension, setup
from torch.utils import cpp_extension

IMPORT_NAME = "itosolver"
MODULE_NAME = "ItoSolver"
INCLUDE_PATH = Path(MODULE_NAME, "include")
DEFAULT_OPT_LEVEL = "-O3"
SUPPORTED_OPT_LEVELS = ["-O0", "-O1", "-O2", "-O3", "-Ofast"]

# Retrieve and set optimisation level
OPT_LEVEL = os.getenv("OPT_LEVEL", DEFAULT_OPT_LEVEL)
if OPT_LEVEL not in SUPPORTED_OPT_LEVELS:
    warnings.warn(
        f"Warning: Unrecognised optimisation level '{OPT_LEVEL}'. "
        f"Defaulting to {DEFAULT_OPT_LEVEL}.",
        UserWarning,
        stacklevel=1,
    )
    OPT_LEVEL = DEFAULT_OPT_LEVEL

# Paths to source files
src_dir = Path(MODULE_NAME, "src")
source_files = [
    src_dir / "euler_maruyama.cpp",
    src_dir / "bindings.cpp",
    src_dir / "ula.cpp",
]

# Define extension module
ext_modules = [
    Extension(
        name=IMPORT_NAME,
        sources=[str(src) for src in source_files],
        include_dirs=[
            str(INCLUDE_PATH),
            pybind11.get_include(),
            *cpp_extension.include_paths(),
        ],
        libraries=["gsl", "gslcblas"],
        library_dirs=cpp_extension.library_paths(),
        language="c++",
        extra_compile_args=[OPT_LEVEL, "-Wall", "-std=c++17", "-fconcepts"],
    ),
]

# Setup configuration
setup(
    ext_modules=ext_modules,
    zip_safe=False,
)
