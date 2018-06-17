#!/usr/bin/env python
from setuptools import setup, find_packages

# Get required packages from requirements.txt
# Make it compatible with setuptools and pip
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="URL Follower",
    version = "1.0.0",
    packages=find_packages(),
    install_requires=requirements
)