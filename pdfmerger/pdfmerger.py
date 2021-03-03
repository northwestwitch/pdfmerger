#!/usr/bin/env python3
import click
import glob
import os
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import io
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def get_page_size(orientation):
    """Returns page width and height (a tuple) given the PDF orientation"""
    width, height = A4
    if orientation == "landscape":  # rotate canvas
        width, height = height, width
    return width, height


def create_watermark(text, orientation):
    """Add a string of text to a PDF file"""
    width, height = get_page_size(orientation)
    packet = io.BytesIO()
    can = canvas.Canvas(packet, (width, height))
    can.setFont("Helvetica", 15)
    can.drawCentredString(width / 2.0, 20, f"{text}")
    can.save()
    # move to the beginning of the StringIO buffer
    packet.seek(0)
    return packet


def validate_infiles(infiles):
    """Checks that each provided file exists on disk"""
    for afile in infiles:
        if os.path.isfile(afile) is False:
            click.echo(f"Incorrect path to file: {afile}")
            raise click.Abort()
        if afile.endswith(".pdf") is False:
            click.echo(f"Incorrect file format: {afile}")
            raise click.Abort()


def concatenate_files_with_watermark(merged, filepaths_n_filenames, orientation):
    """Concatenate original PDF files in the order they were provided after adding a footer with the original file name on each page"""

    # Loop over PDF files provided by user
    for filepath, filename in filepaths_n_filenames:

        # Read original PDF
        existing_pdf = PdfFileReader(open(filepath, "rb"))
        width, height = get_page_size(orientation)

        # Create a new temp file with PDF footer reflecting original PDF name
        wmark = create_watermark(filename, orientation)
        wmark_pdf = tempfile.NamedTemporaryFile(delete=True)
        wmark_pdf = PdfFileReader(wmark)
        wmark_page = wmark_pdf.getPage(0)  # the page with the actual watermark to add

        # Create a blank document and use it to add the watermark to the original PDF file
        blank_pdf = PdfFileWriter()

        # this step might be slow, according to how big the PDFs are and how many pages they contain
        click.echo(f"Adding text to pages from {filename}\n")

        # Add watermark to every page of the original PDF and add the combined page to the output
        npages = existing_pdf.getNumPages()
        for npage in range(0, npages):
            blank_pdf.addBlankPage(width, height)
            blank_page = blank_pdf.getPage(npage)
            blank_page.mergePage(wmark_page)
            blank_page.mergePage(existing_pdf.getPage(npage))

        # write "output" to a new file
        tmp_pdf_with_wmark = tempfile.NamedTemporaryFile(delete=True)
        outputStream = open(tmp_pdf_with_wmark.name, "wb")
        blank_pdf.write(outputStream)
        outputStream.close()

        # Append each temp PDF file with watermark to the merged final PDF
        merged.append(tmp_pdf_with_wmark.name, bookmark=filename)

    return merged


def concatenate_files(merged, filepaths_n_filenames):
    """Concatenate original PDF files in the order they were provided"""

    # Loop over PDF files provided by user
    for filepath, filename in filepaths_n_filenames:
        # Read original PDF
        existing_pdf = PdfFileReader(open(filepath, "rb"))
        merged.append(existing_pdf, bookmark=filename)
    return merged


@click.command()
@click.option(
    "--infile",
    "-f",
    required=True,
    multiple=True,
    help="Path to one infile, repeat for multiple files",
)
@click.option(
    "--orientation",
    type=click.Choice(["portrait", "landscape"]),
    required=True,
    nargs=1,
    help="Orientation of initial PDF files",
)
@click.option(
    "--outfolder",
    type=click.Path(exists=True),
    required=False,
    nargs=1,
    help="Path to destination outfile",
)
@click.option(
    "--outfile",
    type=click.STRING,
    required=False,
    nargs=1,
    help="Name of destination outfile",
    default="pdfmerger_out.pdf",
)
@click.option(
    "--add-filenames",
    default=False,
    is_flag=True,
    help="Write original file names on the pages before merging",
)
def concatenate(infile, orientation, outfolder, outfile, add_filenames):
    """Concatenate all PDF files in a folder and add bookmarks and file watermarks containing with original PDF name"""

    validate_infiles(infile)  # infile is actually a list of files

    # Create a list of tuples consisting in path to PDF with corresponding bookmark (file) name.
    # Example: [('pdfmerger/demo/pdf1.pdf', 'pdf1'), ('pdfmerger/demo/pdf2.pdf', 'pdf2')
    filepaths_n_filenames = [
        (pdf_file, os.path.basename(pdf_file).split(".")[0]) for pdf_file in infile
    ]

    # merge PDF files into one, with bookmarks
    merged = PdfFileMerger()
    click.echo("Merging files, this might take a while..\n")
    if add_filenames:  # Add watermarks with file name to the files before merging them
        merged = concatenate_files_with_watermark(merged, filepaths_n_filenames, orientation)
    else:  # just merge the files in the given order
        merged = concatenate_files(merged, filepaths_n_filenames)

    # Write merged file
    if outfile.endswith(".pdf") is False:
        outfile += ".pdf"
    outpath = os.path.join(outfolder or "", outfile)
    click.echo(f"Writing outfile to: '{outpath}'")
    merged.write(outpath)


def main():
    """Entry point of the program"""
    concatenate()
