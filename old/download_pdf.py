import requests
from PyPDF2 import PdfReader
import re

url = 'https://www.7eleven.com.my/pdf/ar-2017.pdf'

# NOTE the stream=True parameter below
with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open('tmp.pdf', 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            # If you have chunk encoded response uncomment if
            # and set chunk_size parameter to None.
            # if chunk:
            f.write(chunk)

pdf = PdfReader('tmp.pdf')

page_number = 2
page_object = pdf.pages[page_number - 1]


page_text = page_object.extract_text()
print(page_text)