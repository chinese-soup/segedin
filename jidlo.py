#!/usr/bin/env python3
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

from flask_caching import Cache

import importlib
import locale

from datetime import datetime

ZOMATO_API_KEY = "02701b5608a9248628e76ba78dd79992"

locale.setlocale(locale.LC_TIME, "cs_CZ.UTF-8")

def import_modules():
    modules = ["lokal", "usalzmannu", "umansfelda", "za_oponou", "zumbera"]
    imported = []
    for i in modules:
        imported.append(importlib.import_module(i, __name__))

    return imported

app = Flask(__name__)
app.config["STATIC_FOLDER"] = "static"

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
#cache.init_app(app)

imported = import_modules()

@app.route("/", methods=["GET"])
@cache.cached(timeout=2)
def home():
    nazvy = []
    urlka = []
    jidla = []
    datumy = []
    segedin = []

    for y in imported:
        nazev, url, datum, jidlo = y.result()
        nazvy.append(nazev)
        urlka.append(url)
        jidla.append(jidlo)
        datumy.append(datum)

        for i,c in jidlo:
            if "sege" in i.lower():
                segedin.append([i, nazev])

    print("Importing:", nazvy, urlka, jidla, datumy)

    return render_template("home.html", dnesni_datum=datetime.today().strftime("%A %d. %B %Y"), nazvy=nazvy, urlka=urlka, jidla=jidla, datumy=datumy, segedin=segedin)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

