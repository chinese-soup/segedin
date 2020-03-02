#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, codecs
from bs4 import BeautifulSoup


kantyna = requests.get("http://uvrtulejidelna.webnode.cz/sluzby/")
if kantyna is not None and kantyna.status_code == 200:
	html = kantyna.text
	soup = BeautifulSoup(html, 'html.parser')
	doc_url = ""

	for i in soup.find_all("a", href=True):
		odkaz = i["href"]
		if ".doc" in odkaz:
			doc_url = odkaz

	r = requests.get(doc_url, stream=True)
	with open("vrtule.doc", 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk: 
				f.write(chunk)
	from subprocess import check_output

	out = check_output(["catdoc", "vrtule.doc"]).decode("utf-8")
	file = codecs.open("vrtule.txt", "w", "utf-8")
	file.write(out)
	file.close()