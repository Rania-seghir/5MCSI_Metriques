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
   {
    "message": "API rate limit exceeded for 83.142.147.16. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)",
    "documentation_url": "https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting"
}
    
    # Effectuer la requête HTTP pour récupérer les commits
    response = requests.get(url)
    commits_data = response.json()
    
    # Extraire les dates des commits
    commit_dates = [commit['commit']['author']['date'] for commit in commits_data]
    
    # Compter le nombre de commits par minute
    minute_counts = {}
    for date_string in commit_dates:
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minute = date_object.strftime('%Y-%m-%d %H:%M')  # Format pour regrouper les minutes
        if minute in minute_counts:
            minute_counts[minute] += 1
        else:
            minute_counts[minute] = 1
    
    # Préparer les données pour le graphique
    chart_data = [{'minute': minute, 'count': count} for minute, count in sorted(minute_counts.items())]
    
    return render_template('commits.html', chart_data=chart_data)

# Route pour extraire les minutes d'une date
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

if __name__ == "__main__":
  app.run(debug=True)

