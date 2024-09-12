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

<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Graphique des Commits</title>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
  </head>
  <body>
    <h1>Commits Minute par Minute</h1>
    <div id="commits_chart" style="width: 900px; height: 500px;"></div>

    <script>
      // Charger Google Charts
      google.charts.load('current', { packages: ['corechart'] });
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        // Appel à l'API Flask pour récupérer les données des commits
        fetch('/api/commits/')
          .then(response => response.json())
          .then(data => {
            // Préparer les données pour Google Charts
            var dataTable = new google.visualization.DataTable();
            dataTable.addColumn('string', 'Minute');
            dataTable.addColumn('number', 'Nombre de Commits');

            // Ajouter les données reçues à la table
            for (var minute in data) {
              dataTable.addRow([minute.toString(), data[minute]]);
            }

            // Options du graphique
            var options = {
              title: 'Nombre de Commits par Minute',
              hAxis: { title: 'Minute' },
              vAxis: { title: 'Nombre de Commits' },
              legend: 'none',
              colors: ['#76A7FA'],
              bar: { groupWidth: '75%' }
            };

            // Créer le graphique dans la div
            var chart = new google.visualization.ColumnChart(document.getElementById('commits_chart'));
            chart.draw(dataTable, options);
          })
          .catch(error => console.error('Erreur lors de la récupération des données :', error));
      }
    </script>
  </body>
</html>

if __name__ == "__main__":
  app.run(debug=True)

