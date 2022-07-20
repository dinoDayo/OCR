"""
A helper class for file management.
great tutorial: https://victordibia.com/blog/pdf-img/ 

Omodayo Origunwa
07.18.2022
"""

from PyPDF2 import PdfFileWriter, PdfFileReader

import os
import time
import subprocess
from tqdm import tqdm
from multiprocessing import Pool

from PIL import Image
import pytesseract
import numpy as np
from pytesseract import Output
import cv2


class helper:
    def __init__(self):
        self.name = "File Helper"
        self.db = "Google Drive"
        self.img_data_path = os.environ.get("ocrImgData")
        self.pdf_data_path = os.environ.get("ocrPdfData")
        self.client_id = os.environ.get("googleClientID")
        self.client_secret = os.environ.get("googleClientSecret")

    def pdfs_to_imgs(self, img_type="png", method="parallel", resolution=300):
        """
        Converts pdf(s) into a image file(s); pngs or jpgs
        """
        file_list = []
        start_time = time.time()

        # get list of files in pdf directory
        for root, dirs, files in os.walk(self.pdf_data_path):
            for file in files:
                if file.endswith(".pdf"):
                    file_path = os.path.join(root, file)
                    file_list.append(file_path)

        # convert pdfs
        if method == "parallel":
            # create pool of threads to process each pdf in parrallel
            num_processes = 30
            pool = Pool(processes=(num_processes))
            pool.map(
                self.process_pdf,
                zip(
                    file_list,
                    [img_type] * len(file_list),
                    [resolution] * len(file_list),
                ),
            )
            pool.close()
        else:
            for file_path in file_list:
                self.convert_pdf(file_path, img_type, resolution)
        print(f"Last file completed in {time.time() - start_time} seconds")

    def convert_pdf(self, file_path, img_type, resolution):
        """
        Converts each page of a pdf to a separate png image
        """
        file_name = os.path.basename(file_path).split(".")[0]
        output_dir = self.img_data_path
        # execute Ghostscript command, print results
        subprocess.run(
            [
                "gs",
                "-dNOPAUSE",
                "-sDEVICE=jpg" if img_type == "jpg" else "-sDEVICE=png16m",
                f"-r{resolution}",
                f"-sOutputFile={output_dir}/{file_name}-%02d.{img_type}",
                f"{file_path}",
                "-dBATCH",
            ],
            stdout=subprocess.PIPE,
        )

    def process_pdf(self, args):
        file_path, img_type, resolution = args
        self.convert_pdf(
            file_path=file_path,
            # output_dir=self.img_data_path,
            img_type=img_type,
            resolution=resolution,
        )

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
