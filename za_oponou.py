#!/usr/bin/env python3
# coding=utf-8

import requests, sys, re
from datetime import datetime
from bs4 import BeautifulSoup

def get_url():
    return "https://www.restauracezaoponou.cz/"

def get_name():
    return "Za Oponou"

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
    print(denvtydnu)

    dny_array = soup.find_all("h3", {"class": "menu-line-head"})
    box = soup.find_all("table", {"class": "menu-table"})

    items = []

    date = "N/A"

    for i in range(0, len(dny_array)):
        if i == denvtydnu:
            try:
                date = box[i].find_previous_sibling("h3").get_text().strip()
            except:
                pass

            rows = box[i].find_all("tr")
            for row in rows:
                gramaz = row.find("td", {"class": "quantity"})
                jidlo = row.find("td", {"class": "name"})
                cena = row.find("td", {"class": "price"})
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
                    items.append(
                        ["{} ({})".format(jidlo, gramaz), "{}".format(cena)]
                    )

        else:
            continue

        # th = row.find("th", {"class": "dayHeader"})
        # if th is not None:
        #     if str(den) in th.get_text():
        #         is_today = True
        #         date = th.get_text()
        #     else:
        #         is_today = False


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

