import requests
from PyPDF2 import PdfReader
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

url = 'https://www.7eleven.com.my/pdf/ar-2017.pdf'

# NOTE the stream=True parameter below
with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open('../tmp.pdf', 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            # If you have chunk encoded response uncomment if
            # and set chunk_size parameter to None.
            # if chunk:
            f.write(chunk)

pdf = PdfReader('../tmp.pdf')

page_number = 2
page_object = pdf.pages[page_number - 1]

page_text = page_object.extract_text()

# Set up chrome driver
options = Options()
options.add_experimental_option("detach", True)
service = Service("/Users/seowyongtao/Desktop/Chrome_Driver/chromedriver_mac64/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

# Open Chrome
driver.switch_to.window(driver.current_window_handle)
driver.maximize_window()

#Experiment
driver.get('https://www.finsentiment.com/default')

text_box = driver.find_element(By.XPATH, '//*[@id="MainContentPlaceHolder_TextSearchBox"]')
text_box.send_keys(page_text)

button = driver.find_element(By.XPATH, '//*[@id="MainContentPlaceHolder_Button2"]')
button.click()

sentiment_score = driver.find_element(By.XPATH, '//*[@id="MainContentPlaceHolder_LabelSentiment"]')
print(sentiment_score.text)

# Close the chrome driver
driver.quit()