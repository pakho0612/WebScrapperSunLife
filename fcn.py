import re
from pandas import options
import pdfkit
from PyPDF2 import PdfMerger
import sys
import os 

def properFloat(string):
    return float(re.sub('[^0-9\.]+', '', string))

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def pagesToPDF(links, output):
    files = []
    config = pdfkit.configuration(wkhtmltopdf=resource_path('bin\\wkhtmltopdf.exe'))
    for i, url in enumerate(links):
        filename = f"page{i}.pdf"
        pdfkit.from_url(url, filename, configuration=config)
        files.append(filename)

    merger = PdfMerger()
    for file in files:
        merger.append(file)
    merger.write(output)
    merger.close()

##pdfLinks=["google.com","yahoo.com", "ebay.ca"]
##pagesToPDF(pdfLinks, "SunLifeScrapper_output.pdf")