import PyPDF2 as PyPDF2
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import io

# Set up chrome driver
options = Options()
options.add_experimental_option("detach", True)
service = Service("/Users/seowyongtao/Desktop/Chrome_Driver/chromedriver_mac64/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

# Open Chrome
driver.switch_to.window(driver.current_window_handle)
driver.maximize_window()

# Experiment
# driver.get('https://disclosure.bursamalaysia.com/FileAccess/apbursaweb/download?id=186018&name=EA_DS_ATTACHMENTS')

# Get the binary content of the PDF file
# pdf_content = driver.find_element(By.XPATH, "//*").get_attribute("outerHTML").encode("ISO-8859-1")

response = requests.get('https://disclosure.bursamalaysia.com/FileAccess/apbursaweb/download?id=186018&name=EA_DS_ATTACHMENTS')
pdf_content = response.content

# Read the PDF content using PyPDF2
pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))

# Extract the desired page
page_number = 3
page = pdf_reader.getPage(page_number - 1)
text = page.extractText()
print(text)

# Save the extracted page to a new PDF file
# output = PyPDF2.PdfFileWriter()
# output.addPage(page)
#
# with open("page_3.pdf", "wb") as f:
#     output.write(f)


# Close the chrome driver
driver.quit()