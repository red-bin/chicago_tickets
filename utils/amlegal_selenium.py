#!/usr/bin/python

import json

from time import sleep 
from selenium import webdriver

driver = webdriver.Chrome()

url = 'http://library.amlegal.com/nxt/gateway.dll/Illinois/chicago_il/municipalcodeofchicago?f=templates$fn=default.htm$3.0$vid=amlegal:chicago_il'
driver.get(url)

url = 'http://library.amlegal.com/nxt/gateway.dll?f=templates$fn=altmain-nf.htm$3.0'
driver.get(url)

url = 'http://library.amlegal.com/nxt/gateway.dll/Illinois/chicago_il/title9vehiclestrafficandrailtransportati?fn=altmain-nf.htm$f=templates$3.0'
driver.get(url)


xpath = '/html/body/table/tbody/tr/td[2]/div[3]/div/span/a'

chapter_selector = "/html/body/table/tbody/tr/td[2]/div[%s]/div/span/a"

ignores = [27]
xpaths = [ chapter_selector % i for i in range(3,41) if i not in ignores ]

page_sources = []
for xpath in xpaths:
    print(xpath)
    elem = driver.find_element_by_xpath(xpath)
   
    curr_url = driver.current_url
    elem.click()
    new_url = driver.current_url

    if curr_url == new_url:
        continue

    title_xpath = '/html/body/table/tbody/tr/td[2]/div[2]/div'

    page_title = driver.find_element_by_xpath(title_xpath)
    page_sources.append((page_title.text, driver.page_source))

    driver.back()
