#!/usr/bin/env python3
# coding=utf-8

import requests, sys, re
from datetime import datetime
from bs4 import BeautifulSoup

def get_url():
    return "http://www.jidelnaerko.cz/"

def get_name():
    return "Jídelna Erko"

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

    box = soup.find_all("table")

    items = []

    date = "N/A"

    for i in range(0, len(box)):
        if i == denvtydnu:
            try:
                date = box[i].find("div", {"class": "txt_ty"} ).get_text().strip()
            except:
                pass

            rows = box[i].find_all("tr")
            for row in rows:
                #gramaz = row.find("td", {"class": "quantity"})
                tds = row.find_all("td")
                if len(tds) != 0:
                    jidlo = tds[1]
                    cena = tds[2]

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

