#!/usr/bin/env python
from scrape_tables import read_tabs
#!/usr/bin/env python
import pandas as pd
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime
import requests
import sys
import re
from selenium import webdriver

def get_auction_title(auction_num, path = "/Users/Alex/Desktop/coding/6853/table_urls.txt"):
	urls = read_tabs(path)
	auction_url = urls[int(auction_num)-1]
	opts = webdriver.FirefoxOptions()
	opts.headless = True
	driver = webdriver.Firefox(options=opts)
	driver.get(auction_url)
	soup = BeautifulSoup(driver.page_source,"html.parser")
	driver.quit()
	links = soup.find_all('img')
	title = ""
	for link in links:
		try:
			if link["class"][0] == "app-item-info-hori__thumbnail":
				title = link["alt"]
		except:
			pass
	return title

def write_titles(p = "/Users/Alex/Desktop/coding/6853/auction_titles.txt"):
	titles = []
	for i in range(385):
		print(i + 1)
		titles.append(get_auction_title(i+1))
	with open(p, "w") as f:
		for title in titles:
			print(title)
			f.write(title)
			f.write("\n")
	return

if __name__ == "__main__":
	title = get_auction_title(1)
	print (title)
	write_titles()