#!/usr/bin/env python3
# coding=utf-8

import requests, sys, re
from datetime import datetime
from bs4 import BeautifulSoup

def get_url():
    return "http://www.umansfelda.cz/daymenu.php"

def get_name():
    return "U Mansfelda (týdenní menu ze sekce 'Akce' z obrázku)"

def get_file():
    kantyna = []
    with open("helper/mansfeld_ocr.txt") as f:
        kantyna = f.readlines()
    return kantyna

def return_menu(soup):
    date = "N/A"
    items = []
    c = 0
    prev_row = ""
    print(soup)
    for row in soup:
        if row.startswith("+") or row.startswith("*"):
            print("LOL".format(row))
            items.append(["{}".format(row.replace("\n", "")), "?"])
            print("ITEMS", items)
            prev_row = row
        else:
            if row != "\n" and (prev_row.startswith("*") or prev_row.startswith("+")) and "Informace o alergenech" not in row:
                items[-1:][0][0] += row.replace("\n", "")

    print("ITEMS {0}".format(items))
    print("DATE", date)

    return(items, date)


def result():
    try:
        file = get_file()
        nazev = get_name()
        url = get_url()

        menu_list, date = return_menu(file)

        return (nazev, url, date, menu_list)

    except Exception as e:
        print(e)
        return (get_name() + "- Chyba", "", str(e), [])

if __name__ == "__main__":
    file = get_file()
    #bs = prepare_bs(file)

    menu_list, date = return_menu(file)
    print(menu_list)

