"""
A helper class for file management.

Omodayo Origunwa
07.18.2022
"""

from PyPDF2 import PdfFileWriter, PdfFileReader

import os
from PIL import Image
import pytesseract
import numpy as np
from pytesseract import Output
import cv2


class helper:
    def __init__(self):
        self.name = "File Helper"
        self.db = "Google Drive"
        self.data_path_in = os.environ.get("ocrInputDataPath")
        self.data_path_out = os.environ.get("ocrOutputDataPath")
        self.client_id = os.environ.get("googleClientID")
        self.client_secret = os.environ.get("googleClientSecret")

    def split_pdfs(self, filename):
        """
        Splits multi-page PDF into multiple single-paged pdfs
        """
        inputpdf = PdfFileReader(open(filename, "rb"))
        for i in range(inputpdf.numPages):
            output = PdfFileWriter()
            output.addPage(inputpdf.getPage(i))
            with open(f"filename_{i}.pdf", "wb") as outputStream:
                output.write(outputStream)

    def pdf_to_img(self, filename):
        """
        Converts a given pdf into a jpeg image file
        """
        return True
