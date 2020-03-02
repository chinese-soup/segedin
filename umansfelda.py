#!/usr/bin/env python3
# coding=utf-8

import requests, sys, re
from datetime import datetime
from bs4 import BeautifulSoup

def get_url():
    return "http://www.umansfelda.cz/daymenu.php"

def get_name():
    return "U Mansfelda"

def get_file():
    kantyna = requests.get(get_url())
    kantyna.encoding = kantyna.apparent_encoding # WORKAROUND: fix for u mansfelda, nepoužívá realně UTF-8
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
    den = datetime.today().day # TODO: FIX
    date = "N/A"

    #date = soup.find("div", {"class": "tabs"}).

    box = soup.find("table", {"class": "menuTable"})
    items = []
    rows = box.find_all("tr")

    is_today = False
    date = "N/A"

    for row in rows:
        if is_today == True:
            gramaz = row.find("td", {"class": "dishAmount"})
            jidlo = row.find("th", {"class": "dishName"})
            cena = row.find("th", {"class": "dishPrice"})
            #TOOD: redo lol
            try:
                cena = cena.get_text()
            except:
                print("Cena není.")
                cena = "?"

            try:
                gramaz = gramaz.get_text()
            except:
                print("Gramaz neni.")
                gramaz = "N/A"

            try:
                jidlo = jidlo.get_text()
            except:
                print("Gramaz neni.")
                jidlo = "N/A"

            if jidlo != "N/A":
                items.append([jidlo, "{} ({})".format(cena, gramaz)])

        th = row.find("th", {"class": "dayHeader"})
        if th is not None:
            if str(den) in th.get_text():
                is_today = True
                date = th.get_text()
            else:
                is_today = False


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

