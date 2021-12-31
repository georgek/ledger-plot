#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="ledger-plot",
    use_scm_version=True,
    packages=find_packages(),
    python_requires=">=3.8",
    setup_requires=["setuptools_scm"],
    install_requires=[
        "matplotlib",
    ],
    scripts=[
        "plot",
    ],
)
