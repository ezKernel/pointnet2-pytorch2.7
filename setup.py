from setuptools import setup, find_packages
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
import glob
import os

# 设置支持的 CUDA 架构
os.environ["TORCH_CUDA_ARCH_LIST"] = "8.0;8.6;8.9"

_ext_src_root = "_ext_src"
_output_dir = "pointnet2"

# 确保输出目录存在
os.makedirs(_output_dir, exist_ok=True)

# 收集源文件
_ext_sources = glob.glob(f"{_ext_src_root}/src/*.cpp") + glob.glob(f"{_ext_src_root}/src/*.cu")

# 头文件目录
include_dirs = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), _ext_src_root, "include")
]

setup(
    name='pointnet2',
    packages=['pointnet2'],  # 明确指定包
    py_modules=[           # 明确指定模块
        'pointnet2_utils',
        'pointnet2_test',
        'pointnet2_modules'
    ],
    ext_modules=[
        CUDAExtension(
            name='pointnet2._ext',
            sources=_ext_sources,
            include_dirs=include_dirs,
            extra_compile_args={
                "cxx": ["-O2"],
                "nvcc": ["-O2"]
            },
        )
    ],
    cmdclass={
        'build_ext': BuildExtension.with_options(no_python_abi_suffix=True)
    }
)