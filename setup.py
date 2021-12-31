#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="ledger-plot",
    use_scm_version=True,
    packages=find_packages(),
    python_requires=">=3.8",
    py_modules=["ledger_plot"],
    setup_requires=["setuptools_scm"],
    install_requires=[
        "click",
        "matplotlib",
        "PyYAML",
    ],
    entry_points={"console_scripts": ["ledger-plot=ledger_plot:main"]},
)
