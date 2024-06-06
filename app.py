from flask import Flask, render_template, Response
from flask import request
import requests
import threading
import time
import json


app = Flask(__name__)

websites = [
    "https://unsub.ac.id/",
    "https://surabaya.telkomuniversity.ac.id/",
    "https://petra.ac.id/",
    "https://www.ubaya.ac.id/",
    "https://telkomuniversity.ac.id/",
    "https://www.unpak.ac.id/",
    "https://www.unida.ac.id/",
    "https://www.unjani.ac.id/",
    "https://www.ciputra.ac.id/",
    "https://binus.ac.id/malang/",
    "https://www.unnur.ac.id/",
    "https://www.unsur.ac.id/",
    "https://www.pasim.ac.id/",
    "https://unmabanten.ac.id/",
    "https://unpam.ac.id/?d=1",
    "https://www.widyatama.ac.id/",
    "https://unpi-cianjur.ac.id/struktur-unpi",
    "https://www.unfari.ac.id/",
    "https://president.ac.id/",
    "https://unma.ac.id/",
    "https://usbypkp.ac.id/",
    "https://unibi.ac.id/",
    "http://www.iwu.ac.id/",
    "https://unsera.ac.id/",
    "https://utn.ac.id/",
    "https://umt.ac.id",
    "http://www.upj.ac.id/",
    "https://www.unbaja.ac.id/",
    "https://www.iuli.ac.id/",
    "http://unisa.ac.id/",
    "http://www.unfari.ac.id/",
    "https://www.umtas.ac.id/",
    "http://unper.ac.id/",
    "https://www.panca-sakti.ac.id/",
    "https://umbanten.ac.id/",
    "https://utb-univ.ac.id/",
    "https://www.stikesceriabuana.ac.id/",
    "https://siakad.unars.ac.id/spmbfront/program-studi ",
    "http://www.itenas.ac.id/",
    "http://www.ithb.ac.id/",
    "http://www.ibm.ac.id/",
    "http://www.imwi.ac.id/",
    "http://www.institutpendidikan.ac.id/",
    "https://itts.ac.id/",
    "https://ikbisannisa.ac.id/",
    "http://www.sthb.ac.id/",
    "http://sthg.ac.id/",
    "http://www.ekuitas.ac.id/",
    "http://www.sttcirebon.ac.id/",
    "http://www.stietribhakti.ac.id/"
]


website_status = {url: "Unknown" for url in websites}

def check_websites():
    while True:
        for url in websites:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    website_status[url] = "Up"
                else:
                    website_status[url] = "Down"
                print(f"{url}: {website_status[url]}")  # Cetak status ke konsol
            except requests.ConnectionError:
                website_status[url] = "Down"
                print(f"{url}: Down (Connection Error)")  # Cetak status ke konsol
        time.sleep(30)

def stream_website_status():
    def generate():
        while True:
            yield "data: {}\n\n".format(json.dumps(website_status))
            time.sleep(1)  # Mengirim status setiap detik
    return Response(generate(), mimetype='text/event-stream')

@app.route('/')
def index():
    return render_template('index.html', websites=websites, website_status=website_status)

@app.route('/stream')
def stream():
    return stream_website_status()

if __name__ == '__main__':
    threading.Thread(target=check_websites, daemon=True).start()
    app.run(host='0.0.0.0', port=11009)