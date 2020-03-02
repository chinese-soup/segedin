#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
import json

def get_url():
    return None

def get_name():
    return "Švejk restaurant U Pětatřicátníků"

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
    a = soup.find_all("div", { "class": "widget widgetWysiwyg clearfix" })[0].find_all("p")
    return items


def return_date(soup):
    b = soup.find_all("div", { "class": "widget widgetWysiwyg clearfix" })
    b = b[0].find_all("p")[0].text
    b = b.replace("DENNÍ NABÍDKA ", "")
    return(b)

def debug_print(date, menu):
    print(date)

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)
        nazev = get_name()
        url = get_url()
        date = return_date(bs)
        menu_list = return_menu(bs)

        print(date, menu_list)
        return(nazev, url, date, menu_list)

    except Exception as exp:
        print(exp)
        return(get_name() + "- Chyba", "", "", [str(exp)])

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    date = return_date(bs)
    menu_list = return_menu(bs)

    #debug_print(date, menu_list)


# curl -X GET --header "Accept: application/json" --header "user_key: 02701b5608a9248628e76ba78dd79992" "https://developers.zomato.com/api/v2.1/dailymenu?res_id=16513145"