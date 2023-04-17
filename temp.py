from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import mysql.connector
import time
import requests
import PyPDF2
import re
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTTextLine, LTChar, LAParams


def contains_ar(string, company_name):
    if 'ar' in company_name.lower() or 'a-r' in company_name.lower():
        if 'annual report' in string.lower() or 'annualreport' in string.lower() or 'bursa' in string.lower():
            return True
        else:
            return False
    else:
        if 'ar' in string.lower() or 'annual report' in string.lower() or 'annualreport' in string.lower() or 'bursa' in string.lower():
            return True
        else:
            return False

def is_title_or_subtitle(text_line):
    bold_fonts = []

    for character in text_line:
        if isinstance(character, LTChar):
            font_name = character.fontname
            if "Bold" in font_name or "Bd" in font_name or "Condensed" in font_name:
                bold_fonts.append(font_name)

    return len(bold_fonts) / len(text_line) > 0.5


def extract_titles(pdf_path):
    titles = []

    for page_layout in extract_pages(pdf_path, laparams=LAParams()):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    if isinstance(text_line, LTTextLine) and is_title_or_subtitle(text_line):
                        title = text_line.get_text().strip()
                        titles.append(title)

    return titles


def extract_section_between_titles(pdf_path, start_title, end_title):
    text = extract_text(pdf_path)

    word1 = start_title
    word2 = end_title

    pattern = re.compile(r'{}(.*?){}'.format(re.escape(word1), re.escape(word2)), re.DOTALL)
    match = pattern.search(text)

    if match:
        extracted_content = match.group(1).strip()
        return extracted_content
    else:
        no_content = "No match found"
        return no_content


# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="FYP"
)

# Create a cursor object
cursor = conn.cursor()

# Retrieve all values from a table
company_values_query = "SELECT * FROM CompanyDim;"
cursor.execute(company_values_query)

# Fetch the results
results = cursor.fetchall()

# Store the values in a list of tuples
companies = []
for result in results:
    companies.append(result)

# Set up chrome driver
options = Options()
options.add_experimental_option("detach", True)
service = Service("/Users/seowyongtao/Desktop/Chrome_Driver/chromedriver_mac64/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

# Open Chrome
driver.switch_to.window(driver.current_window_handle)
driver.maximize_window()

# Experiment
for company in companies:
    company_id = company[0]
    company_name = company[1]
    company_code = company[2]

    # temporary
    # if company_code in ['5250', '7214']:
    #     print('hey')
    #     continue

    print(company_name)

    url = 'https://www.malaysiastock.biz/Corporate-Infomation.aspx?securityCode=' + str(company_code)

    # Navigate to the page containing the table
    driver.get(url)

    # Find the table element with id 'ctl21_tbCompanyAR'
    table = driver.find_element(By.ID, 'ctl21_tbCompanyAR')

    # Find the first cell in the table by locating its <td> element
    first_cell = table.find_element(By.TAG_NAME, 'td')

    # Use string slicing to get the last 4 characters
    lastest_year = int(first_cell.text[-4:]) + 1
    lastest_year_minus_5 = lastest_year - 5

    if company_code == '7131':
        break


# Close the chrome driver
driver.quit()
