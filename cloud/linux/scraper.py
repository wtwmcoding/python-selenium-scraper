#!/usr/bin/env python

from selenium import webdriver
from pyvirtualdisplay import Display
import random
import mysql.connector
import subprocess
import time

#### EC2 Settings ####
display = Display(visible=0, size=(1024, 768))
display.start()

#### Database settings ####
config = {
  	'user' : 'username',
	'password' : 'password',
	'host' : 'rdsname.endpoint.server.rds.amazonaws.com',
	'database' : 'databasename',
	'charset' : 'utf8',
	'raise_on_warnings' : True,
}
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(buffered=True)

#### Class element ####
className = 'name-of-class-or-id-of-element'

##### Headless Browser Settings #####
options = webdriver.ChromeOptions()
options.add_argument('headless')
path_to_chromedriver = '/path/to/chromedriver' 
driver = webdriver.Chrome(executable_path = path_to_chromedriver,chrome_options = options)

###### Fetch Previous Data ######
urls = []
query = ("SELECT url FROM urls")
cursor.execute(query)
for row in cursor:
	urls.append(row[0])


for url in urls:
	###### Fetch Previous Data ######
	query = ("SELECT idUrl FROM urls WHERE url = '%s'" % (url))
	cursor.execute(query)
	for row in cursor:
		urlId = row[0]
	previous_data = []
	query = ("SELECT String FROM scrapedData WHERE urlId = %d" % (urlId))
	cursor.execute(query)
	for row in cursor:
		previous_data.append(row[0].encode('utf-8'))

	###### Scraper ######
	scraped_data = []
	print("Scraping %d out of %d urls" % (urls.index(url) +1, len(urls))) 
	driver.get(url)
	time.sleep(random.randint(10, 20)) # Scraper buffer
	elems = driver.find_elements_by_class_name(className)
	if not elems:
		continue
	if elems: 
		for elem in elems:
			scraped_data.append(elem.text.encode('utf-8'))

	###### Compare Datasets ######
	d1 = set(previous_data)
	d2 = set(scraped_data)
	d3 = d1.symmetric_difference(d2)
	if list(d1 & d3):
		removedStrings = list(d1 & d3)
		for r in removedStrings:
			query = ("UPDATE scrapedData SET Removed = 'yes' WHERE String = '%s' AND urlId = %d" % (r, urlId)
			cursor.execute(query)
	if list(d2 & d3):
		newStrings = list(d2 & d3)
		for n in newStrings:
			query = ("INSERT INTO scrapedData (urlID, String, Removed) VALUES ('%d', '%s', 'no') % (urlId, n)
			cursor.execute(query)
cnx.commit()
driver.quit()
cursor.close()
cnx.close()
display.stop()