# -*- coding: utf-8 -*-
name = "openvdb"
version = "12.0.1"
authors = ["DreamWorks Animation"]
description = "OpenVDB: Sparse volume data structure and tools."

requires = [
    "boost-1.84.0",
    "tbb-2022.2.0",  # 또는 2021.x
    "zlib-1.2.13",
    "openexr-3.2.2",
    "imath-3.1.9",
    "blosc-1.21.5",
    "nanobind-2.5.0",  # OpenVDB 12.0.1은 nanobind 필요
    "tsl_robin_map-1.3.0",  # nanobind의 의존성
    "python-3.13.2"
    
]

build_requires = [
    "cmake-3.26.5",
    "gcc-11.5.0",
    "python-3.13.2"
    
]

build_command = "python {root}/rezbuild.py {install}"

def commands():
    env.OPENVDB_ROOT = "{root}"
    env.OpenVDB_ROOT = "{root}"
    env.CMAKE_PREFIX_PATH.append("{root}")
    env.PATH.append("{root}/bin")
    env.LD_LIBRARY_PATH.prepend("{root}/lib64")
    env.LIBRARY_PATH.prepend("{root}/lib64")
    env.PKG_CONFIG_PATH.prepend("{root}/lib/pkgconfig")
    env.PYTHONPATH.prepend("{root}/lib64/python3.13/site-packages")    
    env.CPATH.prepend("{root}/include")

