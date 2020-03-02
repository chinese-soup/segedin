#!/usr/bin/env python3
# coding=utf-8

import requests, sys, re
from datetime import datetime
from bs4 import BeautifulSoup

dny = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota", "Neděle"]

def get_url():
    return "http://www.andelcafe.cz/bistro/"

def get_name():
    return "Bistro Anděl"

def get_file():
    headers = {
        "User-Agent": "Mozilla/5.0 (Android 8.0.0; Mobile; rv:61.0) Gecko/61.0 Firefox/68.0",
    }
    kantyna = requests.get(get_url(), headers=headers)
    kantyna.encoding = kantyna.apparent_encoding # WORKAROUND: fix for u mansfelda, nepoužívá realně UTF-8
    print(kantyna.headers)

    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    else:
        return "Error"

def return_menu(soup):
    print(soup)
    import sys
    denvtydnu = datetime.today().weekday()
    date = "N/A"
    container = soup.find("div", {"id": "slider-main"})
    items = []

    dny_v_tydnu = container.find_all("div", {"class": "daymenu-currentday"})

    for den in dny_v_tydnu:
        if den.get_text() == dny[denvtydnu]:
            print("Found it, ", den.get_text())
            box = den.parent
            break

    rows = box.find_all("div", {"class": "daymenu-item"})

    for row in rows:
        print("ROW ==== ", row)
        #gramaz = row.find("td", {"class": "quantity"})
        jidlo = row.find("h3")
        #cena = row.find("td", {"class": "price"})

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
            # items.append(
            #     ["{} ({})".format(jidlo, gramaz), "{}".format(cena)]
            # )
            items.append(
                ["{}".format(jidlo), "{}".format("")]
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

