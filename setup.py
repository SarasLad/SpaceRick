from setuptools import setup, find_packages

setup(
    name="SpaceRick",
    version="0.1.0",
    license="MIT"
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "rich",
        "tqdm",
        "pyfiglet"
    ],
    entry_points={
        "console_scripts": [
            "spacerick=core.main:main",
        ],
    },
    author="Saras Lad",
    description="A modular web vulnerability scanner CLI tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SarasLad/SpaceRick",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)




