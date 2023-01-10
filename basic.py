from flask import Flask, render_template, request
from mongoengine import *
from datetime import datetime

app = Flask(__name__)

connect(host="mongodb://localhost:27017/hto")

class Jednotka(Document):
    jmeno = StringField(required=True, max_length=32)
    prijmeni = StringField(required=True, max_length=32)
    telefon = IntField(required=True)
    datum_odberu = StringField(max_length=32)
    typ_odberu = StringField(required=True)
    objem = IntField(default=450);
    skupina = StringField(default="---", max_length=24)
    rh_fakt = BooleanField()
    sarze = IntField(default=0)
    sluzebnik = IntField(default=0)
    
    objem_ok = BooleanField()
    skupina_ok = BooleanField()
    tuky_ok = BooleanField()
    tlak_ok = StringField(max_length=32)
    vystup_ok = BooleanField()
    
    lokace = StringField(max_length=5)    
    
#produkt = Jednotka(kod="66í7")
#produkt.save()
#produkt.update(barva="read").save()


@app.route('/')
def uvodni_stranka():
    return render_template("index.html", Jednotka=Jednotka.objects)

@app.route('/produkce', methods=["GET", "POST"])
def odber():
    if request.method == "GET":
        return render_template("produkce.html", Jednotka=Jednotka.objects)
    elif request.method == "POST":
        jmeno = request.form["jmeno"]
        prijmeni = request.form["prijmeni"]
        telefon = request.form["telefon"]
        now = datetime.now()
        datum_odberu = now.strftime("%d.%m.%Y")
        objem = request.form["objem"]
        skupina = request.form["skupina"]
        typ_odberu = request.form["typ_odberu"]
        rh_fakt_q = request.form["rh_fakt"]
        if rh_fakt_q == "negativní":
            rh_fakt = 0
        else:
            rh_fakt = 1
        sarze = now.strftime("%y%m%d%H%M%S")
        Jednotka(jmeno=jmeno, prijmeni=prijmeni, telefon=telefon, objem=objem, skupina=skupina, typ_odberu=typ_odberu, rh_fakt=rh_fakt, sarze=sarze, datum_odberu=datum_odberu).save()
        
        return render_template("produkce.html", vzkaz="Záznam založen.", Jednotka=Jednotka.objects)

@app.route('/kontrola', methods=["GET", "POST"])
def kontrola():
    if request.method == "GET":
        return render_template("kontrola.html", Jednotka=Jednotka.objects)
    elif request.method == "POST":
        nazev = request.form["nazev"]
        telefon = request.form["telefon"]
        now = datetime.now()
        datum_odberu = now.strftime("%d.%m.%Y")
        objem = request.form["objem"]
        skupina = request.form["skupina"]
        typ_odberu = request.form["typ_odberu"]
        rh_fakt = request.form["rh_fakt"]
        sarze = now.strftime("%y%m%d%H%M%S")
        Jednotka(nazev=nazev, telefon=telefon, objem=objem, skupina=skupina, typ_odberu=typ_odberu, rh_fakt=rh_fakt, sarze=sarze, datum_odberu=datum_odberu).save()
        
        return render_template("kontrola.html", vzkaz="Záznam založen.", Jednotka=Jednotka.objects)

@app.route('/cekajici', methods=["GET", "POST"])
def cekajici():
    if request.method == "GET":
        return render_template("cekajici.html", Jednotka=Jednotka.objects)
    elif request.method == "POST":
        stitek = request.form["xko"]


if __name__ == "__main__":
    app.run(debug=True)