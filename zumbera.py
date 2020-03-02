#!/usr/bin/env python3
# coding=utf-8

import requests, sys, re
from datetime import datetime
from bs4 import BeautifulSoup

def get_url():
    return "https://www.menicka.cz/api/iframe/?id=2064"

def get_name():
    return "Restaurace Žumbera"

def get_file():
    kantyna = requests.get(get_url())
    #kantyna.encoding = kantyna.apparent_encoding # WORKAROUND: fix for u mansfelda, nepoužívá realně UTF-8
    kantyna.encoding = "windows-1250"
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
    try:
        dnes_span = soup.find("span", {"class": "dnes"})
        container = dnes_span.find_previous("div")
        date = container.find("h2").get_text()
        box = container.find("table", {"class": "menu"})

    except Exception as e:
        print("Error", e)
        return "Chyba"

    items = []

    lines = box.find_all("tr")

    for row in lines:
        #gramaz = row.find("td", {"class": "quantity"})
        jidlo = row.find("td", {"class": "food"})
        cena = row.find("td", {"class": "prize"})
        #TOOD: redo lol
        try:
            cena = cena.get_text()
        except:
            print("Cena není.")
            cena = "?"


        try:
            jidlo = jidlo.get_text()
        except:
            print("Gramaz neni.")
            jidlo = "N/A"

        if jidlo != "N/A":
            items.append(
                ["{}".format(jidlo), "{}".format(cena)]
            )


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

