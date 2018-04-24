#!/usr/bin/env python

from selenium import webdriver
import random
import subprocess
import time
import csv
import os
import datetime

##### Folder and File Settings #####
os.chdir('/path/to/working/directory')
new_dataset_csv = 'new_dataset.csv'
changes_dataset_csv = 'changes_dataset'+datetime.datetime.now().strftime("%m%d%y_%H%M")+'.csv' # Variable storing changes data


##### Headless Browser Settings #####
options = webdriver.ChromeOptions()
options.add_argument('headless')
path_to_chromedriver = '/path/to/chromedriver' 
driver = webdriver.Chrome(executable_path = path_to_chromedriver,chrome_options = options)

###### Variables ######
urls = ['www.example.com/page1','www.example.com/page2','www.example.com/page3']
className = 'name-of-class-or-id-of-element'
new_dataset = []
previous_data = []

###### Fetch Previous Data ######
with open(new_dataset_csv) as csvDataFile:
	csvReader = csv.reader(csvDataFile)
	for r in csvReader:		
		previous_data.append(r[0])

###### Scraper ######
for url in urls:
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
			new_dataset.append(scraped_data)
driver.quit()

###### Compare Datasets ######
changes_dataset = [['Removed','New']]
for url in urls:
	i = urls.index(url)
	d1 = set(previous_data[i])
	d2 = set(new_dataset[i])
	d3 = d1.symmetric_difference(d2)
	changes_row = []
	changes_row.append(list(d1 & d3))
	changes_row.append(list(d2 & d3))
	changes_dataset.append(changes_row)

###### Export data to .csv ######
with open(changes_dataset_csv, 'wb') as csv_file:
	writer = csv.writer(csv_file)
	writer.writerows(changes_dataset)
with open(new_dataset_csv,'wb') as csv_file:
	writer = csv.writer(csv_file)
	writer.writerows(new_dataset)
print("Writing Complete")
subprocess.call(['open', new_dataset_csv])
subprocess.call(['open', changes_dataset_csv])