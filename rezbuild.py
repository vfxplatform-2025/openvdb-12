# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess

def run_cmd(cmd, cwd=None):
    print(f"[RUN] {cmd}")
    subprocess.run(cmd, cwd=cwd, shell=True, check=True)

def clean(path):
    if os.path.exists(path):
        for item in os.listdir(path):
            if item.endswith(".rxt"):
                continue
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
            else:
                os.remove(full_path)

def write_pkgconfig(install_root, version):
    pc_dir = os.path.join(install_root, "lib", "pkgconfig")
    os.makedirs(pc_dir, exist_ok=True)
    pc = f"""\
prefix={install_root}
exec_prefix=${{prefix}}
libdir=${{prefix}}/lib
includedir=${{prefix}}/include

Name: OpenVDB
Description: Sparse volume data storage and IO library
Version: {version}
Requires: Imath
Libs: -L${{libdir}} -lopenvdb
Cflags: -I${{includedir}}
"""
    pc_path = os.path.join(pc_dir, "openvdb.pc")
    with open(pc_path, "w") as f:
        f.write(pc)
    print(f"🔧 Generated pkg-config file: {pc_path}")
    
def build(source_path, build_path, install_path, targets):
    version = os.environ.get("REZ_BUILD_PROJECT_VERSION", "12.0.1")
    src_dir = os.path.join(source_path, f"source/openvdb-{version}")

    clean(build_path)
    if "install" in targets:
        install_path = f"/core/Linux/APPZ/packages/openvdb/{version}"
        clean(install_path)

    os.makedirs(build_path, exist_ok=True)

    run_cmd(
    f"cmake {src_dir} "
    f"-DCMAKE_INSTALL_PREFIX={install_path} "
    f"-DCMAKE_BUILD_TYPE=Release "
    # Blosc 켜기 (옵션 이름이 OPENVDB_USE_BLOSC 입니다)
    f"-DOPENVDB_USE_BLOSC=ON "
    # 바이너리만 빌드, 유닛테스트 OFF
    f"-DOPENVDB_BUILD_BINARIES=ON "
    f"-DOPENVDB_BUILD_UNITTESTS=OFF "
    # Python 바인딩 활성화
    f"-DOPENVDB_BUILD_PYTHON_MODULE=ON "
    # Python 3.13.2 지정 (PYTHON_ 접두사)
    f"-DPYTHON_EXECUTABLE=/core/Linux/APPZ/packages/python/3.13.2/bin/python3 "
    f"-DPYTHON_INCLUDE_DIR=/core/Linux/APPZ/packages/python/3.13.2/include/python3.13 "
    f"-DPYTHON_LIBRARY=/core/Linux/APPZ/packages/python/3.13.2/lib/libpython3.13.so "
    # TBB 경로 명시적 지정 (oneAPI 구조)
    f"-DTBB_ROOT={os.environ['REZ_TBB_ROOT']} "
    f"-DTbb_DIR={os.environ['REZ_TBB_ROOT']}/lib/cmake/tbb "
    f"-DCMAKE_CXX_FLAGS='-DTBB_SUPPRESS_DEPRECATED_MESSAGES=1 -I{os.environ['REZ_TBB_ROOT']}/include/oneapi -I/core/Linux/APPZ/packages/python/3.13.2/include/python3.13 -I{os.environ['REZ_TSL_ROBIN_MAP_ROOT']}/include' "
    # 의존성 루트
    f"-DCMAKE_PREFIX_PATH=\""
      f"{os.environ['REZ_BLOSC_ROOT']};"
      f"{os.environ['REZ_NANOBIND_ROOT']};"
      f"{os.environ['REZ_TSL_ROBIN_MAP_ROOT']};"
      f"{os.environ['REZ_BOOST_ROOT']};"
      f"{os.environ['REZ_TBB_ROOT']};"
      f"{os.environ['REZ_OPENEXR_ROOT']};"
      f"{os.environ['REZ_IMATH_ROOT']}\" "
    "-G Ninja",
    cwd=build_path
)



    run_cmd("cmake --build . --parallel", cwd=build_path)

    if "install" in targets:
        run_cmd("cmake --install .", cwd=build_path)
        write_pkgconfig(install_path, version)
        shutil.copy(os.path.join(source_path, "package.py"), os.path.join(install_path, "package.py"))

    print("✅ OpenVDB build complete")

if __name__ == "__main__":
    build(
        source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
        build_path=os.environ["REZ_BUILD_PATH"],
        install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
        targets=sys.argv[1:]
    )

