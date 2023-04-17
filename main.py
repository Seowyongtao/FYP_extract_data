from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import mysql.connector
import time


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
company_values_query = "SELECT * FROM Company;"
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

    if company_code == '7131':
        break

# Close the chrome driver
driver.quit()
