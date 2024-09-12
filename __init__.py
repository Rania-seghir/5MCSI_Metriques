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
    return render_template("contact.html")
  


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


@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")


# Fonction pour récupérer les commits via l'API GitHub
def get_commits():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur lors de la récupération des commits: {response.status_code}")
        return []

# Fonction pour extraire les minutes des commits
def extract_minutes(commits):
    commit_minutes = []
    for commit in commits:
        date_str = commit['commit']['author']['date']
        date_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        commit_minutes.append(date_object.minute)
    return commit_minutes

# Route pour servir la page HTML
@app.route('/')
def index():
    return render_template('index.html')

# Route API pour renvoyer les données des commits sous forme de JSON
@app.route('/api/commits')
def api_commits():
    commits = get_commits()
    minutes = extract_minutes(commits)
    
    # Compter le nombre de commits par minute
    minute_counts = [0] * 60
    for minute in minutes:
        minute_counts[minute] += 1
    
    return jsonify(minute_counts)

if __name__ == "__main__":
  app.run(debug=True)

