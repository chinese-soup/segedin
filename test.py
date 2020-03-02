#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from bs4 import BeautifulSoup

def get_file():
	kantyna = requests.get("http://www.chutpoint.cz/denni-nabidka/")
	return kantyna

def prepare_bs(kantyna):
	if kantyna is not None and kantyna.status_code == 200:
		html = kantyna.text
		soup = BeautifulSoup(html, 'html.parser')
		return soup

	else:
		return "Error"

def return_menu(soup):
	a = soup.find("div", { "class": "widget widgetWysiwyg clearfix" })
	b = a.findNext("h1")
	c = b.findNext("p").text
	d = re.split(" Kč", c)
	
	items = []
	date = ""

	for i in d:
		if "Nevybrali" not in i:
			if "2016" in i: # pokud je na radku datum, odchytme ho
				a = re.match("(.*?[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4})", i)
				if a is not None:
					date = a.group(1)
					i = i[len(date):]
			
			re_cena = re.match(".*?\s?([0-9]+)$", i)
			if re_cena is not None:
				cena = re_cena.group(1)
				i = i[:-len(cena)]
				items.append([i.rstrip(), str(cena), ""]) # TODO: fix
			else:
				items.append([i.rstrip(), "", ""]) 
			print(i)

	print("ITEMS {0}".format(items))
	print("DATE", date)
	return(items, date)


#def return_date(soup):
#	return("")

def result():
	try:
		file = get_file()

		bs = prepare_bs(file)

		#date = return_date(bs)
		menu_list, date = return_menu(bs)

		return(date, menu_list)
	except Exception as e:
		print(e)
		return(str(e), [])

if __name__ == "__main__":
	file = get_file()

	bs = prepare_bs(file)

	#date = return_date(bs)
	menu_list = return_menu(bs)

	#debug_print(date, menu_list)
