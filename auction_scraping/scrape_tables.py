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

def scrape_bid_table(url, iter_num):
	opts = webdriver.FirefoxOptions()
	opts.headless = True
	driver = webdriver.Firefox(options=opts)
	driver.get(url)
	soup = BeautifulSoup(driver.page_source,"html.parser")
	driver.quit()
	rows = []
	auto_str = "This is an automatic bid (proxy bid) placed by eBay on behalf of the bidder."
	starting_price = "0"
	for tr in soup.find_all('tr')[2:]:
		row = []
		tds = tr.find_all('td')
		for i in range(len(tds)):
			row.append(tds[i].text.strip())
		if len(row) == 3:
			rows.append(row)
		if "Starting Price" in row:
			starting_price = row[1]
	if len(rows) > 0:
		with open("/Users/Alex/Desktop/coding/6853/raw_tables/auction_" + str(iter_num)+".csv", "w") as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(["bidder","bid_amount", "bid_time", "starting_price", "automatic"])
			for row in rows:
				if "Retracted" in row[1]:
					continue
				auto = False
				if "This is an automatic bid (proxy bid) placed by eBay on behalf of the bidder." in row[0]:
					row[0] = row[0].replace("This is an automatic bid (proxy bid) placed by eBay on behalf of the bidder.", "")
					auto = True
				writer.writerow(row + [starting_price] + [auto])




def read_tabs(path):
	urls = []
	with open(path, "r") as f:
		for row in f.readlines():
			urls.append(row.replace("\n",""))
	return urls


if __name__ == "__main__":
	urls =read_tabs("/Users/Alex/Desktop/coding/6853/table_urls.txt")
	for i,url in enumerate(urls):
		scrape_bid_table(url,i+1)
		print (i)






