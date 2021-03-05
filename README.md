# pdfmerger
A small python package to merge and bookmark PDF files based on PyPDF2 and reportlab.

Allows to **merge a list of PDF files while preserving their original name**. In fact the file name of each merged file (without extension) may optionally be written on every page of the merged file (watermark).

Unless specified in the program options (--write-filenames) no watermark will be added to the pages.

Output file will contain **bookmarks** to the original files.

## Running the program using Docker (no installation required)
This program can be used on the fly without installation by running the image present on [Docker Hub](https://hub.docker.com/r/northwestwitch/pdfmerger/tags?page=1&ordering=last_updated)

Simple command to launch the container and check that it works:
```
docker run -it --rm  pdfmerger --help
```
Keep in mind that you need to map the folder(s) containing the files to merge and the folder that will contain the outfile to a folder in the Docker container filesystem (default is /home/pdfmerger/data). To do so you should run the container providing a volume. For instance if you files are in folder `/home/username/documents` the volume will be `/home/username/documents:/home/pdfmerger/data`

Please note that the program will look your for infiles inside `/home/pdfmerger/data` because that is the folder that they're mapped into, so when you run the program from the terminal the --infile(-f) option should point to that folder.
In the terminal, In order to produce an outfile on your file system (and outside the container) you should also provide the option `--outfolder /home/pdfmerger/data`.

Example command to pull the image from Docker Hub and execute the program directly with custom parameters:
```
docker run -d --rm \
-v /home/username/documents:/home/pdfmerger/data \
northwestwitch/pdfmerger --orientation landscape \
-f /home/pdfmerger/data/infile1.pdf -f /home/pdfmerger/data/infile2.pdf \
--outfolder /home/pdfmerger/data (--outfile outfilename.pdf)
```

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
Options:
  -f, --infile TEXT               Path to one infile, repeat for multiple
                                  files  [required]

  --orientation [portrait|landscape]
                                  Orientation of initial PDF files  [required]
  --outfolder PATH                Path to destination outfile
  --outfile TEXT                  Name of destination outfile
  --write-filenames               Write original file names on the pages
                                  before merging
  --help                          Show this message and exit.
```

Example:
```
pdfmerge --orientation landscape -f infile1.pdf -f infile2.pdf .. --add-filenames (--outfolder outfolder --outfile outfile.pdf)
```

The demo folder contains [3 test files](https://github.com/northwestwitch/pdfmerger/tree/master/pdfmerger/demo) that you could test the program with.
