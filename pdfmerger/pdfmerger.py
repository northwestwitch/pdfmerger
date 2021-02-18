#!/usr/bin/env python3
import click
import glob
import os
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import io
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def create_footer(footer_text):
    """Add a string of text to a PDF file"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(25, 25, f" -- {footer_text} --")
    can.save()
    # move to the beginning of the StringIO buffer
    packet.seek(0)
    return packet


@click.command()
@click.argument("infolder", type=click.Path(exists=True), required=True)
@click.option(
    "--outfolder",
    type=click.Path(exists=True),
    required=False,
    nargs=1,
    help="Path to destination outfile",
)
@click.option(
    "--outname",
    type=click.STRING,
    required=False,
    nargs=1,
    help="Name of destination outfile",
    default="pdfmerger_out.pdf",
)
def concatenate(infolder, outfolder, outname):
    """Concatenate all PDF files in a folder and add bookmarks and file footers with original PDF name"""

    pdf_files = sorted(glob.glob(os.path.join(infolder, "*.pdf")))

    # Create a list of tuples consisting in path to PDF with corresponding bookmark name
    files_n_filenames = [
        (pdf_file, os.path.basename(pdf_file).split(".")[0]) for pdf_file in pdf_files
    ]

    # merge PDF files into one, with bookmarks
    merged = PdfFileMerger()

    # Loop over PDF files contained in folder
    for item in files_n_filenames:

        # Create a new temp file with PDF footer
        footer_content = create_footer(item[1])
        tmp_footer = tempfile.NamedTemporaryFile(delete=True)
        tmp_footer = PdfFileReader(footer_content)

        # Read original PDF
        existing_pdf = PdfFileReader(open(item[0], "rb"))

        # add the "watermark" (which is the new pdf) on the existing page
        output = PdfFileWriter()
        page = existing_pdf.getPage(0)
        page.mergePage(tmp_footer.getPage(0))
        output.addPage(page)

        # write "output" to a new file
        tmp_pdf_with_footer = tempfile.NamedTemporaryFile(delete=True)
        outputStream = open(tmp_pdf_with_footer.name, "wb")
        output.write(outputStream)
        outputStream.close()

        # Append each temp PDF file with footer to the merged final PDF
        merged.append(tmp_pdf_with_footer.name, bookmark=item[1])

    # Write merged file
    merged.write(os.path.join(outfolder or "", outname))


def main():
    """Entry point of the program"""
    concatenate()
