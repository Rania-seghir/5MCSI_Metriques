from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #comm2

@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"
  
if __name__ == "__main__":
  app.run(debug=True)

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/rapport/")
def mongraphique():
    # Retourner le fichier HTML
    return render_template("graphique.html")

@app.route("/rapport/data/")
def rapport_data():
    # Simuler des données pour l'exemple
    data = {
        "results": [
            {"Jour": 1638316800, "temp": 15},
            {"Jour": 1638403200, "temp": 16},
            {"Jour": 1638489600, "temp": 14},
            {"Jour": 1638576000, "temp": 17},
        ]
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

