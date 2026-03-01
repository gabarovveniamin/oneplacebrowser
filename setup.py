from setuptools import setup, find_packages

setup(
    name="CometBrowser",
    version="0.1.0",
    description="A powerful browser built with Python and PyQt6",
    author="Developer",
    author_email="dev@example.com",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.6.1",
        "PyQt6-WebEngine>=6.6.0",
        "requests>=2.31.0",
        "lxml>=4.9.3",
        "beautifulsoup4>=4.12.2",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "comet-browser=src.main:main",
        ],
    },
)
