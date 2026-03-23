"""Setup script for OmniNet v4."""

from setuptools import setup, find_packages

setup(
    name="omninet-v4",
    version="4.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "omninet=omninet.daemon:main",
            "omninet-verify=omninet.math:verify_mathematics",
        ],
    },
    python_requires=">=3.8",
)
