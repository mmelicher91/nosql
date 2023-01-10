from flask import Flask, render_template, request, redirect, url_for
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
    skupina = StringField(default="---", max_length=24)
    rh_fakt = StringField(max_length=10)
    sarze = IntField(default=0)
    sluzebnik = IntField(default=0)
    
    objem = IntField(default=0);
    tuky_ok = BooleanField(default=False)
    tlak = StringField(max_length=32)
    tlak_ok = BooleanField(default=False)
    zaver_ok = StringField(max_lenght=32)
    
     
    
#produkt = Jednotka(kod="66í7")
#produkt.save()
#produkt.update(barva="read").save()


@app.route('/')
def uvodni_stranka():
    return render_template("index.html", Jednotka=Jednotka.objects)

@app.route('/produkce', methods=["GET", "POST"])
def produkce():
    if request.method == "GET":
        return render_template("produkce.html", Jednotka=Jednotka.objects)
    elif request.method == "POST":
        jmeno = request.form["jmeno"]
        prijmeni = request.form["prijmeni"]
        telefon = request.form["telefon"]
        now = datetime.now()
        datum_odberu = now.strftime("%d.%m.%Y")
        skupina = request.form["skupina"]
        typ_odberu = request.form["typ_odberu"]
        rh_fakt = request.form["rh_fakt"]
        sarze = now.strftime("%y%m%d%H%M%S")
        Jednotka(jmeno=jmeno, prijmeni=prijmeni, telefon=telefon, skupina=skupina, typ_odberu=typ_odberu, rh_fakt=rh_fakt, sarze=sarze, datum_odberu=datum_odberu).save()
        
        return render_template("produkce.html", vzkaz="Záznam založen.", Jednotka=Jednotka.objects)

@app.route('/kontrola', methods=["GET", "POST"])
def kontrola():
    print("###########")
    #pacient = request.args["pacient_id"]
    if request.method == "GET":
        pacient = request.args["pacient_id"]
        vysledek=Jednotka.objects(id=pacient).first()
        jmeno = vysledek.jmeno
        prijmeni = vysledek.prijmeni
        sarze = vysledek.sarze
        skupina = vysledek.skupina
        rh_fakt = vysledek.rh_fakt
        typ_odberu = vysledek.typ_odberu
        zaz_id = vysledek.id

        return render_template("kontrola.html", jmeno=jmeno, prijmeni=prijmeni, sarze=sarze, skupina=skupina, rh_fakt=rh_fakt, typ_odberu=typ_odberu, zaz_id=zaz_id)
               
    elif request.method == "POST":
        kontrolni = 0
        p_id =request.form["zaz_id"]
        objem = request.form["objem"]
        q_tuky = request.form["tuky_ok"]
        if q_tuky == "nok":
            tuky_ok = False
            kontrolni +=1
        else:
            tuky_ok = True
        tlak = request.form["tlak"]
        q_tlak = request.form["tlak_ok"]
        if q_tlak == "nok":
            tlak_ok = False
            kontrolni +=1
        else:
            tlak_ok = True

        q_zaver = request.form["zaver_ok"]
        if q_zaver == 'ok' and kontrolni == 0:
            zaver_ok = "Vyhovuje"
            sluzebnik = 1
        else:
            zaver_ok = "Vyřazen"
            sluzebnik = 2
        Jednotka.objects(id=p_id).update(objem=objem, tuky_ok=tuky_ok, tlak_ok=tlak_ok, zaver_ok=zaver_ok, sluzebnik=sluzebnik)

        return render_template("kontrola.html", vzkaz="Záznam upraven.", Jednotka=Jednotka.objects)

@app.route('/cekajici', methods=["GET", "POST"])
def cekajici():
    if request.method == "GET":
        return render_template("cekajici.html", Jednotka=Jednotka.objects)
    elif request.method == "POST":
        pacient_id = request.form["pacient"]
        print("Vybrany pacient")
        print(pacient_id)
        return redirect(url_for("kontrola", pacient_id=pacient_id, Jednotka=Jednotka.objects))

if __name__ == "__main__":
    app.run(debug=True)