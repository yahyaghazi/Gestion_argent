#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de configuration du package pour l'application de Gestion Financière et de Stock.
"""

from setuptools import setup, find_packages

with open("docs/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="finance_stock_app",
    version="1.0.0",
    author="Kata King",
    author_email="kata.king.78@gmail.com",
    description="Application de gestion financière et de stock",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kata-king/finance_stock_app",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: French",
        "Topic :: Office/Business :: Financial",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "finance-stock-app=app.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json"],
        "app": ["assets/*"],
    },
)