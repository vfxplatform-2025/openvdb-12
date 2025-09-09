# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Rez-based build configuration for OpenVDB 12.0.1. OpenVDB is an open-source C++ library for sparse volumetric data structures developed by DreamWorks Animation.

## Build System Architecture

### Key Components

1. **Rez Package Management**: Uses Rez 3.2.1 for dependency resolution and environment management
2. **CMake Build**: Utilizes CMake with Ninja generator for the actual compilation
3. **Python Integration**: Builds Python bindings using pybind11 for Python 3.13.2

### File Structure

- `package.py`: Rez package definition specifying dependencies and environment setup
- `rezbuild.py`: Main build script that orchestrates CMake configuration and compilation
- `get_source.sh`: Downloads OpenVDB source from GitHub releases
- `source/`: Directory where OpenVDB source code is extracted

## Build Commands

### Complete Build Process for OpenVDB 12.0.1

```bash
# 1. Download source code
./get_source.sh

# 2. Build using Rez (from parent directory)
cd ..
rez-build --install

# Or build in isolated environment
rez-env openvdb -- rez-build --install
```

### Manual Build Steps

```bash
# Download and extract source
./get_source.sh

# Set up build environment with dependencies
rez-env boost-1.84.0 tbb-2021.11.0 zlib-1.2.13 openexr-3.2.2 imath-3.1.9 blosc-1.21.5 pybind11-2.11.1 python-3.13.2 cmake-3.26.5 gcc-11.5.0

# Run the build
python rezbuild.py install
```

## Dependencies

### Runtime Dependencies (from package.py)
- boost-1.84.0
- tbb-2022.2.0
- zlib-1.2.13
- openexr-3.2.2
- imath-3.1.9
- blosc-1.21.5
- nanobind-2.5.0 (OpenVDB 12.0.1 uses nanobind instead of pybind11)
- python-3.13.2

### Build Dependencies
- cmake-3.26.5
- gcc-11.5.0
- python-3.13.2

## Build Configuration Details

The `rezbuild.py` script configures OpenVDB with:
- **Build Type**: Release
- **Blosc Compression**: Enabled (`OPENVDB_USE_BLOSC=ON`)
- **Binaries**: Built (`OPENVDB_BUILD_BINARIES=ON`)
- **Unit Tests**: Disabled (`OPENVDB_BUILD_UNITTESTS=OFF`)
- **Python Module**: Enabled (`OPENVDB_BUILD_PYTHON_MODULE=ON`)
- **Python Version**: 3.13.2 (hardcoded paths to `/core/Linux/APPZ/packages/python/3.13.2`)
- **Install Path**: `/core/Linux/APPZ/packages/openvdb/12.0.1`

## Environment Variables Set by Package

When the package is resolved, it sets:
- `OPENVDB_ROOT` and `OpenVDB_ROOT`: Package root directory
- `CMAKE_PREFIX_PATH`: For CMake to find OpenVDB
- `PATH`: Adds `{root}/bin`
- `LD_LIBRARY_PATH` and `LIBRARY_PATH`: Adds `{root}/lib64`
- `PKG_CONFIG_PATH`: Adds `{root}/lib/pkgconfig`
- `PYTHONPATH`: Adds `{root}/lib64/python3.13/site-packages`
- `CPATH`: Adds `{root}/include`

## Troubleshooting

### Source Download Issues
- The script downloads from: `https://github.com/AcademySoftwareFoundation/openvdb/archive/refs/tags/v12.0.1.tar.gz`
- Archives are validated and re-downloaded if corrupted
- Source is extracted to `source/openvdb-12.0.1/`

### Build Failures
- Ensure all Rez dependencies are available and properly installed
- Check that Python 3.13.2 is installed at `/core/Linux/APPZ/packages/python/3.13.2`
- Verify CMake can find all dependencies through `CMAKE_PREFIX_PATH`

### Clean Build
The build script automatically cleans build directories before building:
- Removes all non-.rxt files from build path
- Cleans install directory when installing

## Build Requirements

OpenVDB 12.0.1은 nanobind-2.5.0이 필요합니다. nanobind가 먼저 빌드되어 있어야 합니다.

### 주요 변경사항
- **Python Binding**: pybind11 대신 nanobind 사용
- **TBB**: 2022.2.0 버전은 oneAPI 구조, 특별한 경로 설정 필요

## Version Updates

To update OpenVDB version:
1. Edit `VERSION` in `get_source.sh`
2. Update `version` in `package.py`
3. Update default version in `rezbuild.py` (line 44)
4. Adjust dependencies in `package.py` if needed for new version requirements