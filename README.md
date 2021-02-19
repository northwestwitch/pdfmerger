# pdfmerger
A small python package to merge and bookmark PDF files based on PyPDF2 and reportlab.

Allows you to **merge a list of PDF files while preserving their original name**. In fact the file name of each merged file (without extension) will be written on top of each merged file.

Creates also **bookmarks** to the original files.

## Installation
Requires python>=3.6.

Clone this repository with the command:
```
git clone https://github.com/northwestwitch/pdfmerger.git
```
enter the created folder with
```
cd pdfmerger
```
Install the software and its dependencies with `pip install`:
```
pip install -e .
```

## Usage

```
Command line options:
  -f, --infile TEXT  Path to one infile, repeat for multiple files  [required]
  --outfolder PATH   Path to destination outfile [optional]
  --outfile TEXT     Name of destination outfile [optional]
```

Example:

`pdfmerge --infile infile1.pdf --infile infile2.pdf .. (--outfolder outfolder --outfile outfile.pdf)`

The demo folder contains [3 test files](https://github.com/northwestwitch/pdfmerger/tree/master/pdfmerger/demo) that you could test the program with.
