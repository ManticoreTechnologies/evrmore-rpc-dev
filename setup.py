#!/usr/bin/env python3
from setuptools import setup, find_packages
import os
import re

# Read version from __init__.py
with open(os.path.join("evrmore_rpc", "__init__.py"), "r") as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string")

# Read long description from README.md
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="evrmore-rpc",
    version=version,
    description="A high-performance Python wrapper for Evrmore blockchain RPC commands with a seamless API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Manticore Technologies",
    author_email="dev@manticore.tech",
    url="https://github.com/manticore-tech/evrmore-rpc",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
    ],
    extras_require={
        "dev": [
        ],
        "zmq": [
        ],
        "all": [
        ]
    },
    entry_points={
        "console_scripts": [
            "evrmore-rpc-stress=evrmore_rpc.stress_test:main",
        ],
    },
    keywords="evrmore blockchain cryptocurrency rpc json-rpc async seamless-api zmq assets",
    project_urls={
        "Bug Reports": "https://github.com/manticore-tech/evrmore-rpc/issues",
        "Source": "https://github.com/manticore-tech/evrmore-rpc",
        "Documentation": "https://github.com/manticore-tech/evrmore-rpc/blob/main/README.md",
    },
) 