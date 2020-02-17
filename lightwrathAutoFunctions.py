from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expCon
from selenium.webdriver.common.by import By

import time

driver = webdriver.Firefox(executable_path="/mnt/RAID/personal/Code/Selenium/geckodriver")

driver.get('http://lightwrath.com')
time.sleep(3)

#Function taking input of the navigation bar text, then selecting that option within the Iframe, returning to default frame after.
def navBarSelector(navBarSelection):
   navFrame = driver.find_element_by_tag_name('iframe')
   print("Switching to ", navFrame)
   driver.switch_to.frame(navFrame)
   navProjectsLocation = "//li[contains(text(), '{}')]".format(navBarSelection)
   navProjectsSelector = WebDriverWait(driver, 10).until(expCon.presence_of_element_located((By.XPATH, navProjectsLocation)))
   print("Clicking ", navBarSelection)
   navProjectsSelector.click()
   driver.switch_to.default_content()

#Function to cycle through links on the projects page.
def projectLinks():
   linkCount = driver.find_elements_by_css_selector('.buttonIcon a')
   for i in range(len(linkCount)):
      try:
         links = driver.find_elements_by_css_selector('.buttonIcon a')
         #linkSelector = WebDriverWait(driver, 10).until(expCon.presence_of_element_located((By.TAG_NAME,links[i])))
         links[i].click()
         time.sleep(1)
         driver.back()
         time.sleep(1)
      except: 
         print(i, "link not detected for: ", links[i])

#Function to submit information via the contact form.
def sentContact(cName, cEmail, cSubject, cMessage):
   nameTag = driver.find_element_by_name('Name')
   emailTag = driver.find_element_by_name('E-mail')
   subjectTag = driver.find_element_by_name('Subject')
   messageTag = driver.find_element_by_name('Message')
   sendButton = driver.find_element_by_name('SEND MESSAGE')
   nameTag.send_keys(cName)
   emailTag.send_keys(cEmail)
   subjectTag.send_keys(cSubject)
   messageTag.send_keys(cMessage)
   time.sleep(1)
   sendButton.click()
   formSpreeReturn = WebDriverWait(driver, 10).until(expCon.presence_of_element_located((By.LINK_TEXT, "Return to original site")))
   formSpreeReturn.click()

#Main
navBarSelector("Contact")
time.sleep(2)
sentContact("Selenium_Test", "lightwrath@live.com", "Selenium Test", "This is a test from Selenium")
time.sleep(2)
navBarSelector("Projects")
time.sleep(2)
projectLinks()
