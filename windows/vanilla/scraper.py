from selenium import webdriver
import random
import subprocess
import time
import csv
import os

##### Folder and File Settings #####
os.chdir(r'/path/to/working/directory')
exported_file = 'exported_file.csv'

##### Headless Browser Settings #####
options = webdriver.ChromeOptions()
options.add_argument('headless')
path_to_chromedriver = r'/path/to/chromedriver' 
driver = webdriver.Chrome(executable_path = path_to_chromedriver,chrome_options = options)

###### Variables ######
urls = ['www.example.com/page1','www.example.com/page2','www.example.com/page3']
className = 'name-of-class-or-id-of-element'
new_dataset = []

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

###### Export data to .csv #####
with open(exported_file,'w', newline='') as csv_file:
	writer = csv.writer(csv_file)
	writer.writerows(new_dataset)
print("Writing Complete")
subprocess.call(r'/path/to/exported_file', shell=True)