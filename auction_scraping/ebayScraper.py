#!/usr/bin/env python
from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime
import requests
import sys
import re

def get_auction_urls(links):
	article_urls = []
	for link in links:
		try:
			if link["class"][0] == "vip":
				article_urls.append(link["href"])
		except:
			pass
	return article_urls


def get_bid_history_urls(links):
	iids = set()
	bids_urls = []
	for url in links:
		page = requests.get(url).content
		soup = BeautifulSoup(page, "lxml")
		hrfs = soup.find_all('a')
		for link in hrfs:
			try:
				if link["class"][0] == "nodestar-item-card-details__view-link":
					s = link["href"]
					if "SellLikeItem&item=" in s:
						subs_A = "SellLikeItem&item="
						subs_B = "&rt=nc&_trksid="
						iid = s[(s.index(subs_A)+len(subs_A)):s.index(subs_B)]
						iids.add(iid)
			except:
				pass
	for iid in iids:
		bids_urls.append("https://www.ebay.com/bfl/viewbids/392281464598?item=" + iid +"&rt=nc&_trksid=p2047675.l2565&showauto=true")
	return bids_urls



def write_bidurls(bid_table_urls):
	with open("/Users/Alex/Desktop/coding/6853/table_urls.txt", "w") as f:
		for url in bid_table_urls:
			f.write(url + "\n")
			
if __name__ == "__main__":
	try:
		page = sys.argv[1]
	except:
		page = "12"
	bid_table_urls = set()
	pg_urls = set()
	for page in range(1,int(page)):
		print(page)
		if page != 1:
			url = "https://www.ebay.com/sch/i.html?_from=R40&_sacat=0&LH_Sold=1&_udlo=&_udhi=&LH_Auction=1&LH_ItemCondition=3&_samilow=&_samihi=&_sadis=15&_stpos=02460&_sop=12&_dmd=1&LH_Complete=1&_fosrp=1&_nkw=Xbox+One+S+1Tb&_pgn="+str(page)+"&_skc="+str(50*(page-1))+"&rt=nc"
		else:
			url = "https://www.ebay.com/sch/i.html?_from=R40&_sacat=0&LH_Sold=1&_udlo=&_udhi=&LH_Auction=1&LH_ItemCondition=3&_samilow=&_samihi=&_sadis=15&_stpos=02460&_sop=12&_dmd=1&LH_Complete=1&_fosrp=1&_nkw=Xbox+One+S+1Tb&rt=nc"

		page = requests.get(url).content
		soup = BeautifulSoup(page, "lxml")
		links = soup.find_all('a')
		article_urls = get_auction_urls(links)
		pg_urls.update(article_urls)
		bid_history_urls = get_bid_history_urls(article_urls)
		bid_table_urls.update(bid_history_urls)
		print("found",len(bid_history_urls), "out of", len(article_urls))
		print(len(bid_table_urls))
		print(len(pg_urls))
	write_bidurls(bid_table_urls)







