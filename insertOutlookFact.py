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
    if company_code in ['5250', '7214']:
        print('hey')
        continue

    print(company_name)

    for year in range(2017, 2022):

        annual_report_links = []

        url = 'https://www.malaysiastock.biz/Corporate-Infomation.aspx?securityCode=' + str(company_code)

        # go to the url
        driver.get(url)
        time.sleep(3)

        # Get the link of the annual report
        try:
            ar = driver.find_element(By.CSS_SELECTOR,
                                     "#divAR_" + str(company_code) + "_" + str(year) + " a:nth-of-type(5)")

            ar_text = ar.get_attribute("text")

            if contains_ar(ar_text, company_name):
                annual_report_links.append(ar.get_attribute("href"))
        except:
            pass

        try:
            ar = driver.find_element(By.CSS_SELECTOR,
                                     "#divAR_" + str(company_code) + "_" + str(year) + " a:nth-of-type(4)")

            ar_text = ar.get_attribute("text")

            if contains_ar(ar_text, company_name):
                annual_report_links.append(ar.get_attribute("href"))
        except:
            pass

        try:
            ar = driver.find_element(By.CSS_SELECTOR,
                                     "#divAR_" + str(company_code) + "_" + str(year) + " a:nth-of-type(3)")

            ar_text = ar.get_attribute("text")

            if contains_ar(ar_text, company_name):
                annual_report_links.append(ar.get_attribute("href"))
        except:
            pass

        try:
            ar = driver.find_element(By.CSS_SELECTOR,
                                     "#divAR_" + str(company_code) + "_" + str(year) + " a:nth-of-type(2)")

            ar_text = ar.get_attribute("text")

            if contains_ar(ar_text, company_name):
                annual_report_links.append(ar.get_attribute("href"))
        except:
            pass

        try:
            ar = driver.find_element(By.CSS_SELECTOR,
                                     "#divAR_" + str(company_code) + "_" + str(year) + " a")

            ar_text = ar.get_attribute("text")

            if contains_ar(ar_text, company_name):
                annual_report_links.append(ar.get_attribute("href"))
        except:
            pass

        # Print the ar link
        print(annual_report_links)

        if len(annual_report_links) > 1:

            for index, url in enumerate(annual_report_links):

                pdf_name = 'tmp' + str(index + 1) + '.pdf'
                print(pdf_name)
                print(url)

                # NOTE the stream=True parameter below
                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    with open(pdf_name, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            # If you have chunk encoded response uncomment if
                            # and set chunk_size parameter to None.
                            # if chunk:
                            f.write(chunk)

            # Open the PDF files you want to merge
            pdf_file1 = open('tmp1.pdf', 'rb')
            pdf_file2 = open('tmp2.pdf', 'rb')

            # Create a new PDF reader object for each file
            pdf_reader1 = PyPDF2.PdfReader(pdf_file1)
            pdf_reader2 = PyPDF2.PdfReader(pdf_file2)

            # Create a new PDF writer object to write the merged PDF files
            pdf_writer = PyPDF2.PdfWriter()

            # Add the pages from the first PDF file to the writer object
            for page_num in range(len(pdf_reader1.pages)):
                page_obj = pdf_reader1.pages[page_num]
                pdf_writer.add_page(page_obj)

            # Add the pages from the second PDF file to the writer object
            for page_num in range(len(pdf_reader2.pages)):
                page_obj = pdf_reader2.pages[page_num]
                pdf_writer.add_page(page_obj)

            # Create a new PDF file and write the merged PDF pages to it
            merged_pdf = open('merged_file.pdf', 'wb')
            pdf_writer.write(merged_pdf)

            # Close all the file objects
            pdf_file1.close()
            pdf_file2.close()
            merged_pdf.close()

        elif len(annual_report_links) == 1:

            url = annual_report_links[0]

            # NOTE the stream=True parameter below
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open('merged_file.pdf', 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        # If you have chunk encoded response uncomment if
                        # and set chunk_size parameter to None.
                        # if chunk:
                        f.write(chunk)

        else:
            pass

        pdf_paths = ["merged_file.pdf"]
        target_section_keywords = ["outlook & prospects", "outlook and strategic", "outlook and prospect",
                                   "moving into 2",
                                   "looking ahead to", "looking ahead for", "looking forward", "moving forward",
                                   "forward-looking",
                                   "looking ahead", "outlook", "future prospects", "prospect", "future"]

        for pdf_path in pdf_paths:
            titles = extract_titles(pdf_path)

            titles_cleaned = []

            for item in titles:
                # Check if the item contains only digits or digits followed by a period (.)
                if not re.match("^\d+\.?$", item):
                    # Check if the item contains any of the specific words or substrings
                    if not re.search("(cont|bhd|berhad)", item, re.IGNORECASE):
                        titles_cleaned.append(item)


            target_title_index = None
            for keyword in target_section_keywords:
                for i, title in enumerate(titles_cleaned):
                    if keyword in title.lower():
                        target_title_index = i
                        break
                if target_title_index is not None:
                    break

            try:
                target_title = titles_cleaned[target_title_index]
                next_title = titles_cleaned[target_title_index + 1]

                section = extract_section_between_titles(pdf_path, target_title, next_title)
                print(f"Extracted section from {pdf_path}:")
                print(section)
                print()

                # Retrieve year id
                company_values_query = "SELECT * FROM TimeDim WHERE year = " + str(year) + ";"
                cursor.execute(company_values_query)

                # Get year ID
                result = cursor.fetchall()
                yearID = result[0][0]

                add_data = ("INSERT INTO OutlookFact"
                            "(CompanyID, TimeID, outlook_text)"
                            "VALUES (%s, %s, %s)")

                cursor.execute(add_data, (company_id, yearID, section))
                # Commit the changes
                conn.commit()

            except (IndexError, TypeError):
                print(f"No matching section found in {pdf_path}")
                print()

                # Retrieve year id
                company_values_query = "SELECT * FROM TimeDim WHERE year = " + str(year) + ";"
                cursor.execute(company_values_query)

                # Get year ID
                result = cursor.fetchall()
                yearID = result[0][0]

                add_data = ("INSERT INTO OutlookFact"
                            "(CompanyID, TimeID, outlook_text)"
                            "VALUES (%s, %s, %s)")

                cursor.execute(add_data, (company_id, yearID, 'none'))
                # Commit the changes
                conn.commit()


    if company_code == '7131':
        break

# Close the cursor and connection
cursor.close()
conn.close()

# Close the chrome driver
driver.quit()