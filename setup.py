import os
import warnings
from pathlib import Path

import pybind11
from setuptools import Extension, setup

# Constants and configuration
MODULE_NAME = "itosolver"
INCLUDE_PATH = Path("include")
DEFAULT_OPT_LEVEL = "-O3"
SUPPORTED_OPT_LEVELS = ["-O0", "-O1", "-O2", "-O3", "-Ofast"]

# Retrieve and set optimisation level
OPT_LEVEL = os.getenv("OPT_LEVEL", DEFAULT_OPT_LEVEL).upper()
if OPT_LEVEL not in SUPPORTED_OPT_LEVELS:
    warnings.warn(
        f"Warning: Unrecognised optimisation level '{OPT_LEVEL}'. "
        f"Defaulting to {DEFAULT_OPT_LEVEL}.",
        UserWarning,
    )
    OPT_LEVEL = DEFAULT_OPT_LEVEL

# Paths to source files
src_dir = Path("src")
source_files = [src_dir / "euler_maruyama.cpp",
                src_dir / "euler_maruyama_py.cpp",
]

# Define extension module
ext_modules = [
    Extension(
        name=MODULE_NAME,
        sources=[str(src) for src in source_files],
        include_dirs=[
            str(INCLUDE_PATH),
            pybind11.get_include(),
            '/usr/include/eigen3',
        ],
        libraries=["gsl", "gslcblas"],
        language="c++",
        extra_compile_args=[OPT_LEVEL, "-Wall", "-std=c++17"],
    ),
]

# Setup configuration
setup(
    ext_modules=ext_modules,
    zip_safe=False,
)
