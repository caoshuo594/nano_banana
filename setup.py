#!/usr/bin/env python3
"""
Setup script for NanoBanana MCP Server
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="nano-banana-mcp",
    version="1.0.0",
    author="NanoBanana",
    description="MCP Server for AI Image Generation using Gemini 3 Pro Image Preview",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/caoshuo594/nano_banana",
    packages=find_packages(),
    py_modules=["mcp_server"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "nano-banana=mcp_server:main",
        ],
    },
)
