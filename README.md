# python-selenium-scraper
Scrape data from specific classes given a URL. Run the script from a cloud instance and store the data into a mySQL database.

# Table of Contents

### 1. Getting Started
* Installation and Requirements
* How Do I Setup On a Local Computer?
* How Do I Setup On a Cloud Instance?
### 2. Running
* Run Using a Command Line Interface (CLI)
* Run Using a Shebang (Unix)
### 3. Applications for Production
* Monitor Changes in Data
* Connect and Store to mySQL Database
* Automate Script on a Schedule
### 4. Conclusion

# 1. Getting Started
Please refer back to this section of the guide in case you get stuck with the setup process.
## Installation and Requirements
Follow the guidelines and instructions below to install python and python's package installer, pip. 
### Technical Requirements:
* Windows 7, 8, 10/Mac OS/Linux
* Python 2.7+
* Command Language Interpreter or shell
* Text Editor

### Skill Requirements:
* Basic knowledge and familiarity with a programming language
* Basic knowledge of command lines

### Installing Python on Mac OS / Linux
"Python comes pre-installed on Mac OS X so it is easy to start using. However, to take advantage of the latest versions of Python, you will need to download and install newer versions alongside the system ones. The easiest way to do that is to install one of the binary installers for OS X from the Python Download page. Installers are available for the latest Python 3 and Python 2 releases that will work on all Macs that run Mac OS X 10.5 and later." - [https://legacy.python.org/download/mac/](https://legacy.python.org/download/mac/)

"Python comes preinstalled on most Linux distributions, and is available as a package on all others." -[https://docs.python.org/3/using/unix.html](https://docs.python.org/3/using/unix.html)

### Installing Python on Windows
Go to [https://legacy.python.org/download/](https://legacy.python.org/download/) and download the 2.7.6 Windows Installer release. You may wish to download the latest release, however it may limit compatibility with software in this project.

### Installing pip

Open up the shell and enter the following commands:
```
sudo apt update
sudo apt-get install python-pip
sudo pip install --upgrade pip
```
`sudo apt update` downloads the package lists from the repositories and "updates" them to get information on the newest versions of packages and their dependencies.

`sudo apt-get install python-pip` installs and manages Python packages

### Install Selenium
Enter the following command:
```
sudo pip install selenium
```
Selenium should now be installed.

### Download chromedriver
Go to [https://sites.google.com/a/chromium.org/chromedriver/downloads] and download the latest release. (Version 2.37 used in this project)
Extract the chromedriver file.

### Download scraper.py
Download the `scraper.py` file in this repository.

## How Do I Setup On a Local Computer?
Once you have the steps above completed, open `scraper.py` in your text editor. The following steps refer to lines and elements in this file.
Replace the folder path of `'/path/to/working/directory'` to the path containing `scraper.py` on the following line:
```
os.chdir('/path/to/working/directory')
```
Replace the file path of `'exported_file.csv'` to the csv file you wish to export the data to in your working folder on the following line:
```
exported_file = 'exported_file.csv'
```
Replace the folder path of `'/path/to/chromedriver'` to the path containing the chromedriver file you downloaded on the following line:
```
path_to_chromedriver = '/path/to/chromedriver' 
```
Replace the strings in the `urls` list with the url(s) you wish to scrape.

Replace the `className` variable with the class name of the element you wish to scrape.

Save `scraper.py`
## How Do I Setup On a Cloud Instance?
Working
# 2. Running
Please refer to this section for information about the lines in the script.

### Crawler
Here is the excerpt of the crawler from the script:
```
for url in urls:
	print("Crawling %d out of %d urls" % (urls.index(url) +1, len(urls))) 
	driver.get(url)
	time.sleep(random.randint(10, 20)) # Scraper buffer
	elems = driver.find_elements_by_class_name(className)
	if not elems:
		continue
	if elems: 
		for elem in elems:
			scraped_data.append(elem.text.encode('utf-8'))
driver.quit()
```
For every url provided by the user, the browser will open the url by `driver.get(url)`, wait a random amount of time, and search the loaded page for the element containing the class by `driver.find_elements_by_class_name(className)`

If the element is found, the string will be added to a list `.append(elem.text.encode('utf-8'))`

Once all the urls have been crawled, the browser will close.

## Run Using a Command Line Interface (CLI)
Run the python script by entering the following on the command line (make sure you are in the correct directory):
```
python scraper.py
```
## Run Using a Shebang (Unix)
With `#!/usr/bin/env python` in the first line of the script, you can double click the file as long as you have the following enabled:
Working
# 3. Applications for Production
## Monitor Changes in Data
Working
## Connect and Store to mySQL Database
Working
## Automate Script on a Schedule
Working
# 4. Conclusion
Working
