from selenium import webdriver

options = webdriver.EdgeOptions()
options.add_argument('--headless')
driver = webdriver.Edge()

url = "https://docs.google.com/spreadsheets/d/1L4yjLKLaMQQokcvFhDzepPWEyGQhhnxnpq7VgPZB0bc/edit?pli=1#gid=0"
driver.get(url)
driver.implicitly_wait(10)
driver.save_screenshot("C:\\dumpster\\KeyforPythonGoogleSheets\\googlesheetsScreenshot.png")
driver.quit
"""This idea of taking a screenshot of the google sheets was a bust because google doesnt like you 
logging in through automation so I had to try and just use my google api stuff and format that in a nice way."""
