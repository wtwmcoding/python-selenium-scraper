# python-selenium-scraper
Scrape data from specific classes given a URL. Run the script from a cloud instance and store the data into a mySQL database.

# Table of Contents

### 1. Getting Started
* Installation and Requirements
* How Do I Setup On a Local Computer?
* How Do I Setup On a Cloud Instance?
### 2. Running
* Run Using a Command Line Interface (CLI)
* Run as an Executable (Unix)
### 3. Developing for Production
* Monitor Changes in Data On Local Computer
* Monitor Changes in Data On mySQL Database
* Automate Script on a Schedule (Unix)
### 4. Conclusion
### 5. Authors
### 6. Credits
### 7. License

# 1. Getting Started
Please refer back to this section of the guide in case you get stuck with the setup process.
## Installation and Requirements
Follow the guidelines and instructions below to install python and python's package installer, pip. 
### Technical Requirements:
* Windows 7, 8, 10/Mac OS/Linux
* Chrome
* Python 2.7+
* Command Language Interpreter or shell
* Text Editor

### Skill Requirements:
* Basic knowledge and familiarity with a programming language
* Basic knowledge of command lines

### Installing Python on Mac OS / Linux
> "Python comes pre-installed on Mac OS X so it is easy to start using. However, to take advantage of the latest versions of Python, you will need to download and install newer versions alongside the system ones. The easiest way to do that is to install one of the binary installers for OS X from the Python Download page. Installers are available for the latest Python 3 and Python 2 releases that will work on all Macs that run Mac OS X 10.5 and later." - [https://legacy.python.org/download/mac/](https://legacy.python.org/download/mac/)

> "Python comes preinstalled on most Linux distributions, and is available as a package on all others." -[https://docs.python.org/3/using/unix.html](https://docs.python.org/3/using/unix.html)

### Installing Python on Windows
Go to [https://legacy.python.org/download/](https://legacy.python.org/download/) and download the 2.7.6 Windows Installer release. You may wish to download the latest release, however it may limit compatibility with software in this project.

### Installing pip
If setting up on a cloud instance, skip this step for now.

Open up the shell and enter the following commands:
```
$ sudo apt update
$ sudo apt-get install python-pip
$ sudo pip install --upgrade pip
```
`sudo apt update` downloads the package lists from the repositories and "updates" them to get information on the newest versions of packages and their dependencies.

`sudo apt-get install python-pip` installs and manages Python packages

### Install Selenium
If setting up on a cloud instance, skip this step for now.

Enter the following command:
```
$ sudo pip install selenium
```
Selenium should now be installed.

### Download chromedriver
Go to [https://sites.google.com/a/chromium.org/chromedriver/downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads) and download the latest release. (Version 2.37 used in this project)
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
Create a Linux instance on AWS for free following the steps listed here:
[https://aws.amazon.com/getting-started/tutorials/launch-a-virtual-machine/](https://aws.amazon.com/getting-started/tutorials/launch-a-virtual-machine/)

You can then connect to your instance via ssh.

You may also connect to your instance via FTP to easily transfer files between your local computer and the instance.

Follow the instructions above to install pip then enter the following commands:
```
$ sudo apt-get install xvfb xserver-xephyr vnc4server
$ sudo pip install pyvirtualdisplay
```
Extract and upload the latest chromedriver to your instance via FTP then enter the following command:
```
$ chmod +x chromedriver
```
Install selenium as instructed above.

Enter the following commands to install chrome:
```
$ sudo apt-get install libnss3
$ sudo apt-get install chromium-browser
```
Upload `scraper.py` to your instance via FTP.

Since your scraped data cannot be easily managed on a cloud instance (e.g. MS Excel), follow the instructions below for exporting data to a database.

# 2. Running
Please refer to this section for information about the lines in the script.

### Scraper
Here is the excerpt of the scraper from the script:
```
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
```
For every url provided by the user, the browser will open the url by `driver.get(url)`, wait a random amount of time, and search the loaded page for the element containing the class by `driver.find_elements_by_class_name(className)`

If the element is found, the string will be added to a list `.append(elem.text.encode('utf-8'))`

Once all the urls have been scraped, the browser will close.

## Run Using a Command Line Interface (CLI)
Run the python script by entering the following on the command line (make sure you are in the correct directory):
```
python scraper.py
```
## Run as an Executable (Unix)
With `#!/usr/bin/env python` in the first line of the script, you can double click the file to run from finder as long as you have the following:

Rename `scraper.py` to `scraper.command`

Open terminal and run:
```
chmod +x scraper.command
```
You should now be able to run the command from finder.
# 3. Developing for Production
## Monitor Changes in Data On Local Computer
The following section works if you have a csv reader (e.g. MS Excel) installed on your operating system. If you're on a Linux system, refer to the next section about storing data to a database. 

To compare data from different periods, we must add a timestamp for each dataset we collect.

To do this, we need to add a new module, called `datetime`
```
import datetime
```
At the end of this section we're going to export two files named `new_dataset.csv` and `changes_datasetMDY_HM.csv` stored in variables named `new_dataset_csv` and `changes_dataset_csv` respectively.

Initially, `new_dataset.csv` should contain all the data from `exported_file.csv`. To do this, run vanilla `scraper.py` once and/or rename `exported_file.csv` to `new_dataset.csv`. **Once the scraper runs with the data comparison code, `new_dataset.csv` will be overwritten and you cannot access the data from previous time periods unless you saved a copy of `new_dataset.csv`**

`changes_datasetmdy_HM.csv` will contain all the data that has changed exporting with a timestamp in the filename where `m` = Month, `d` = Day, `y` = Year, `H` = Hour, `M` = Minute. This is retrieved from the command `datetime.datetime.now().strftime("%m%d%y_%H%M")`. For the purposes of this project, we will compare whether the scraped data is 'removed' or 'new'. *Edited data will count as a net change, storing the previous value in 'removed' and the current value in 'new'.*

Before the scraper code runs, we're going to create a new list, called `previous_data` that is going to store the current values in `new_dataset.csv`:
```
previous_data = []
with open(new_dataset_csv) as csvDataFile:
	csvReader = csv.reader(csvDataFile)
	for r in csvReader:		
		previous_data.append(r[0])
```
After the scraper code is executed, we're going to compare the previous data with the scraped data:
```
changes_dataset = [['Removed','New']]
for url in urls:
	i = urls.index(url)
	d1 = set(previous_data[i])
	d2 = set(scraped_data[i])
	d3 = d1.symmetric_difference(d2)
	changes_row = []
	changes_row.append(list(d1 & d3))
	changes_row.append(list(d2 & d3))
	changes_dataset.append(changes_row)
```
Then we're ready to export the changes by adding more lines of code to export:
```
with open(changes_dataset_csv, 'wb') as csv_file:
	writer = csv.writer(csv_file)
	writer.writerows(changes_dataset)
```
If you want to open the new exported files once the script is complete, add the following:
```
subprocess.call(['open', new_dataset_csv])
subprocess.call(['open', changes_dataset_csv])
```
## Monitor Changes in Data On mySQL Database
Instead of managing your data by csv, you can use mySQL. Using a mySQL database will be more effective and efficient for managing your data as you can associate different properties to each value you scrape.

*Disclaimer: As a beginner to mySQL and having only setup AWS RDS once, I recommend following the official docs from AWS and mySQL workbench to setup the database.*

YMMV, but the following is how I proceeded from an AWS/EC2 instance.

### Requirements
* Basic fundamentals of SQL
* mySQL Database
* mySQL Workbench (You may wish to ssh into the database, but I found this the most effective)

### Setting up a mySQL Database through Amazon RDS
Follow the steps to create and connect to a mySQL Database: [https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.MySQL.html](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.MySQL.html)

Setup the inbound rules in the security group settings for your database through Amazon to be accessed from your local IP address.

Follow the steps to connect to your database from mySQL workbench:
[https://aws.amazon.com/premiumsupport/knowledge-center/connect-rds-mysql-workbench/](https://aws.amazon.com/premiumsupport/knowledge-center/connect-rds-mysql-workbench/)

Tips that helped me get through the setup:
* Write down any usernames/passwords that you created during the steps above
* Write down the endpoints/hostnames that are created from the steps above
* Errors most likely came from setting up the inbound rules incorrectly.

Once you connect to the database from mySQL workbench, create and initialize the tables in your database. This will depend on how you wish to setup your data.

For example, you can create separate tables storing the urls and scraped data:

**Table: urls**

| idUrl  | url           | domain    |
| -------|:-------------:|:---------:|
| 1      | example.com   | example   |
| 2      | domainname.com| domainname|
| 3      | abcdomain.com | abcdomain |

**Table: scrapedData**

| idScraped | urlId | String    | Removed |
| --------- |:-----:|:---------:| ------- |
| 1         | 2     | 'Hello'   | no      |
| 2         | 2     | 'World!'  | no      |
| 3         | 3     | '1234567' | yes     |

You may also set your tables to auto increment with each new entry. 

In your shell, enter the following commands:
```
$ sudo pip install mysql-connector
```

With the tables created, we can now code the connection to the database in our script:
```
import mysql.connector
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
```
We can now proceed with querying the database for the urls and scraped data to use in our script:
```
urls = []
query = ("SELECT url FROM urls")
cursor.execute(query)
for row in cursor:
	urls.append(row[0])
for url in urls:
	query = ("SELECT idUrl FROM urls WHERE url = '%s'" % (url))
	cursor.execute(query)
	for row in cursor:
		urlId = row[0]
	previous_data = []
	query = ("SELECT String FROM scrapedData WHERE urlId = %d" % (urlId))
	cursor.execute(query)
	for row in cursor:
		previous_data.append(row[0].encode('utf-8'))
```
The scraper code works similarly to the code for running it locally, however with the line `new_dataset.append(scraped_data)` removed as we no longer need to export a dataset to a csv. The data comparison code is also similar with a few changes:
```
for url in urls:
	.
	.
	.
	d1 = set(previous_data)
	d2 = set(scraped_data)
	d3 = d1.symmetric_difference(d2)
	### Data Comparison Changes Start ###
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
	### Data Comparison Changes End ###
```
Once all the change queries have been made, we can commit the changes to the database with the following line:
```
cnx.commit()
```

You can now access your data via mySQL workbench or other SQL query tools.

## Automate Script on a Schedule (Unix)
We can run the script at scheduled times using cron jobs.

On your CLI, run the following command to view a list of cron jobs:
```
crontab -l
```
Run the following command to edit your cron jobs:
```
crontab -e
```
This will open up a text editor in your shell called vi. Here you can add/edit/delete cron jobs.
You'll want to add a line similar to below, save, and exit the vi:
```
* * * * * python /path/to/scraper.py > /path/to/output.log 2>&1
```
This line of code is understood as:
* Every minute, run the following command:
* `python /path/to/scraper.py`
* Export the standard output to `/path/to/output.log`

You can also use [https://crontab-generator.org/](https://crontab-generator.org/) to make a crontab easier.

# 4. Conclusion
Thank you for viewing my project. I'm proud to say that I worked on this project alone even though I had zero experience with python, AWS, EC2, RDS, and mySQL before I started this project in March 2018. I started this project to automate a tedious task for my job and to add experience to my developer career.

### But How Did I Do It?
Despite my lack of prior experience with the language and tools used in this project, I wasn't intimidated to go forward with it. I taught myself javascript through freeCodeCamp which helped me understand the code formatting in python. I also took a course at my university that required students to ssh into a computer at my professor's lab.

Whenever I got stuck, I studied the fundamentals. I researched stackoverflow, a lot. I googled things, a lot. I executed code by trial and error, a lot. 

The most difficult part about this project for me was setting up the security rules on AWS. There aren't any step-by-step guides in the official docs or any formal lessons that I could find. Also, this was probably the least code-related step. However my prior experience plugging the ethernet cable in the wrong ports on my home router helped me visualize what needed to be done. In short, I thought of it as there are digital input and output plugs on your internet connection that can connect with the digital input and output plugs on the RDS database and EC2 instance.

### YMMV
I was lucky enough to have a Mac, enabling me to use *Unix bash commands* in the *terminal shell*. None of these terms would have been as clear and easy to me if I were to have started this project on Windows. That being said, you can still run the project on Windows (YMMV) but it's ideal for production use on a Unix system.
# 5. Authors
* **Matthew Galang** - *All Work* - Me!
# 6. Credits
The following guides inspired me to start this project:

* [Webscraping with Selenium by Thiago Marzagão](http://thiagomarzagao.com/2013/11/12/webscraping-with-selenium-part-1)
* [Setup Cloud-based Data Scraping for Free using AWS by @raoshashank](https://medium.com/@raoshashank/free-cloud-based-data-scraping-using-aws-e111a950e6b5)

Thank you Thiago and Shashank!
# 7. License
This project is licensed under the MIT License - see the [](LICENSE.md) file for details
