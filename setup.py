import io
import os
from setuptools import setup
from pdfmerger.__version__ import VERSION

# Package meta-data.
NAME = "pdfmerger"
DESCRIPTION = "A small python package to merge and bookmark PDF files based on PyPDF2"
URL = "https://github.com/northwestwitch/pdfmerger"
EMAIL = "rasi.chiara@gmail.com"
AUTHOR = "Chiara Rasi"
KEYWORDS = ["PDF", "PyPDF2", "reportlab", "merge", "concatenate", "bookmark", "footer", "name"]
LICENSE = "MIT"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

here = os.path.abspath(os.path.dirname(__file__))


def parse_reqs(req_path="./requirements.txt"):
    """Recursively parse requirements from nested pip files."""
    install_requires = []
    with io.open(os.path.join(here, "requirements.txt"), encoding="utf-8") as handle:
        # remove comments and empty lines
        lines = (line.strip() for line in handle if line.strip() and not line.startswith("#"))

        for line in lines:
            # check for nested requirements files
            if line.startswith("-r"):
                # recursively call this function
                install_requires += parse_reqs(req_path=line[3:])

            else:
                # add the line as a new requirement
                install_requires.append(line)

    return install_requires


# Collect packages that are required for this module
REQUIRED = parse_reqs()

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": ["pdfmerger = pdfmerger.pdfmerger:main"],
    },
    install_requires=REQUIRED,
)
