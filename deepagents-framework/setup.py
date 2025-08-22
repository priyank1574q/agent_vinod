#!/usr/bin/env python3
"""
Setup script for DeepAgents Framework
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="deepagents-framework",
    version="1.3.0",
    author="DeepAgents Team",
    author_email="contact@deepagents.ai",
    description="A powerful AI agent framework built with LangGraph and Amazon Bedrock",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/deepagents-framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "ipykernel>=6.25.0",
        ],
        "database": [
            "sqlalchemy>=2.0.0",
            "psycopg2-binary>=2.9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "deepagents=core.main:main",
            "deepagents-bedrock=core.main_bedrock:main",
        ],
    },
    include_package_data=True,
    package_data={
        "deepagents": [
            "data/*.csv",
            "coding_prompt/*.md",
            "docs/*.md",
        ],
    },
)
