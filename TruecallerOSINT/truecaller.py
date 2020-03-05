from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox(
        firefox_profile = "< Add your firefox profile path here >",
        executable_path = "./geckodriver"
    )

number = "<put number here>"

driver.get("https://www.truecaller.com/search/in/{0}".format(number))

# name = driver.find_element_by_xpath("//main//header//h1/text()").text
name_element = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, "//main//header//h1"))
)
name = name_element.text

print("Name: {}".format(name))
