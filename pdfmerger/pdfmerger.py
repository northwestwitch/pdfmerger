#!/usr/bin/env python3
import click
import glob
import os
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import io
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_watermark(text):
    """Add a string of text to a PDF file"""
    (width, height) = letter
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont('Helvetica', 15)
    can.drawCentredString(width / 2.0, width + 120, f" ## {text} ##")
    can.save()
    # move to the beginning of the StringIO buffer
    packet.seek(0)
    return packet

def validate_infiles(infiles):
    """Checks that each privided file exists on disk"""
    for afile in infiles:
        if os.path.isfile(afile):
            continue
        click.echo(f"Incorrect path to file: {afile}")
        raise click.Abort()

@click.command()
@click.option('--infile', '-f', required=True, multiple=True, help="Path to one infile, repeat for multiple files")
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
def concatenate(infile, outfolder, outfile):
    """Concatenate all PDF files in a folder and add bookmarks and file watermarks containing with original PDF name"""

    validate_infiles(infile) # infile is actually a list of files

    # Create a list of tuples consisting in path to PDF with corresponding bookmark (file) name.
    # Example: [('pdfmerger/demo/pdf1.pdf', 'pdf1'), ('pdfmerger/demo/pdf2.pdf', 'pdf2')
    filepaths_n_filenames = [
        (pdf_file, os.path.basename(pdf_file).split(".")[0]) for pdf_file in infile
    ]

    # merge PDF files into one, with bookmarks
    merged = PdfFileMerger()

    # Loop over PDF files contained in folder
    for filepath, filename in filepaths_n_filenames:

        # Read original PDF
        existing_pdf = PdfFileReader(open(filepath, "rb"))

        # Create a new temp file with PDF footer
        wmark = create_watermark(filename)
        wmark_pdf = tempfile.NamedTemporaryFile(delete=True)
        wmark_pdf = PdfFileReader(wmark)

        # add the "watermark" (which is the new pdf) on the existing page
        output = PdfFileWriter()
        page = wmark_pdf.getPage(0)
        page.mergePage(existing_pdf.getPage(0))
        output.addPage(page)

        # write "output" to a new file
        tmp_pdf_with_wmark = tempfile.NamedTemporaryFile(delete=True)
        outputStream = open(tmp_pdf_with_wmark.name, "wb")
        output.write(outputStream)
        outputStream.close()

        # Append each temp PDF file with watermark to the merged final PDF
        merged.append(tmp_pdf_with_wmark.name, bookmark=filename)

    # Write merged file
    if outfile.endswith(".pdf") is False:
        outfile += ".pdf"
    outpath = os.path.join(outfolder or "", outfile)
    click.echo(f"Writing outfile to: '{outpath}'")
    merged.write(outpath)


def main():
    """Entry point of the program"""
    concatenate()
