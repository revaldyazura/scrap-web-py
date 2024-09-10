from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.request import urlopen

link = 'https://quotes.toscrape.com/'

driver = webdriver.Chrome()
driver.get((link))

def parse_read(driver=driver):
  soup = BeautifulSoup(driver.page_source, "html.parser")
  text = soup.find_all("span", class_="text")
  for obj in text:
      print(obj.get_text())

for x in range(1, 10):
  current_page_url = driver.current_url
  print(f"Page {x}: ")
  parse_read(driver=driver)
  try:
    next_button = driver.find_element(By.CSS_SELECTOR, f"a[href='/page/{x+1}/']")
    next_button.click()
  except:
    print(f"Last page at page {x}.")
    break