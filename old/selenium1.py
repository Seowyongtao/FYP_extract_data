from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_experimental_option("detach", True)

service = Service("/Users/seowyongtao/Desktop/Chrome_Driver/chromedriver_mac64/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.amazon.com/fire-tv-stick-4k-max-with-alexa-voice-remote/dp/B09BS25XWH?th=1")
id = driver.find_element(By.ID,"acrCustomerReviewText")
print(id.text)

css = driver.find_element(By.CSS_SELECTOR, "#feature-bullets ul li .a-list-item")
print(css.text)

xpath = driver.find_element(By.XPATH, '//*[@id="nav-subnav"]/a[7]/span')
print(xpath.text)

driver.quit()