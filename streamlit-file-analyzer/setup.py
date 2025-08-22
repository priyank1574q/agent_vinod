#!/usr/bin/env python3
"""
Setup script for Streamlit File Analyzer
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="streamlit-file-analyzer",
    version="1.4.0",
    author="File Analyzer Team",
    author_email="contact@fileanalyzer.ai",
    description="Interactive web application for file analysis with Amazon Bedrock AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/streamlit-file-analyzer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Framework :: Streamlit",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "enhanced": [
            "altair>=5.0.0",
            "pydeck>=0.8.0",
            "watchdog>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "file-analyzer=app_bedrock:main",
        ],
    },
    include_package_data=True,
    package_data={
        "streamlit_file_analyzer": [
            "sample_data/*",
            "credentials/aws_credentials_template.json",
        ],
    },
    scripts=[
        "start_app.sh",
    ],
)
