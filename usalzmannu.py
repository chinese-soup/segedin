#!/usr/bin/env python3
# coding=utf-8

import requests, sys, re
from datetime import datetime
from bs4 import BeautifulSoup

def get_url():
    return "https://www.usalzmannu.com/cz/denni-nabidka/"

def get_name():
    return "U Salzmannů"

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

    date = soup.find("div", {"class": "tabs"}).find("li", {"class": "active"}).find("a").get_text()

    box = soup.find("div", {"class": "active"})
    tables = box.find_all("table")

    items = []

    for table in tables:
        lokal_rows = table.find_all("tr")

        for row in lokal_rows:
            (gramaz, jidlo, cena) = row.find_all("td")
            (gramaz, jidlo, cena) = (gramaz.get_text(), jidlo.get_text(), cena.get_text())
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

