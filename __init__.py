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


# Route pour récupérer et afficher les commits
@app.route('/commits/')
def commits():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie que la requête a réussi
        commits_data = response.json()
    except requests.exceptions.RequestException as e:
        return f"Erreur de récupération des données : {e}", 500

    # Extraire les dates des commits
    commit_dates = [commit['commit']['author']['date'] for commit in commits_data]
    
    # Compter le nombre de commits par minute
    minute_counts = {}
    for date_string in commit_dates:
        try:
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
            minute = date_object.strftime('%Y-%m-%d %H:%M')  # Format pour regrouper les minutes
            if minute in minute_counts:
                minute_counts[minute] += 1
            else:
                minute_counts[minute] = 1
        except ValueError:
            continue  # Ignore les dates au format incorrect
    
    # Préparer les données pour le graphique
    chart_data = [{'minute': minute, 'count': count} for minute, count in sorted(minute_counts.items())]
    
    return render_template('commits.html', chart_data=chart_data)

# Route pour extraire les minutes d'une date
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    try:
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})
    except ValueError:
        return jsonify({'error': 'Format de date invalide'}), 400


if __name__ == "__main__":
  app.run(debug=True)

