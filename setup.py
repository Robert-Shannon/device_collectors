from setuptools import setup, find_packages

setup(
    name="device_collectors",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "bleak>=0.19.0",
        "asyncio>=3.4.3",
        "PyYAML>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.20.0",
        ],
    },
)
