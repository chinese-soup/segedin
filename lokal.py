#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from datetime import datetime
from bs4 import BeautifulSoup

def get_url():
    return "http://lokal-poddivadlem.ambi.cz/cz/"

def get_name():
    return "Lokál Pod Divadlem"

def get_file():
    kantyna = requests.get(get_url())
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    else:
        return "Error"

def return_menu(soup):
    denvtydnu = datetime.today().weekday()

    date = soup.find("span", {"class": "date"}).get_text()
    lokal_box = soup.find("img", {"alt": "Lokál Pod Divadlem"})
    lokal_table = lokal_box.parent.parent.find("table")
    lokal_rows = lokal_table.find_all("tr")
    items = []
    for row in lokal_rows:
        (jidlo, cena) = row.find_all("td")
        (jidlo, cena) = (jidlo.get_text(), cena.get_text())
        if "Kč" in cena:
            items.append([jidlo, cena])

    print("ITEMS {0}".format(items))
    print("DATE", date)

    return(items, date)


def result():
    try:
        file = get_file()
        bs = prepare_bs(file)

        nazev = get_name()
        url = get_url()

        menu_list, date = return_menu(bs)

        return (nazev, url, date, menu_list)

    except Exception as e:
        print(e)
        return (get_name() + "- Chyba", "", str(e), [])

if __name__ == "__main__":
    file = get_file()
    bs = prepare_bs(file)
    menu_list = return_menu(bs)

