from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

URLS = {
    "devices": "https://context-pre.apsevilla.com/v2/entities?limit=1000&offset=0&options=count&idPattern=.*&type=Device",
    "alerts": "https://context-pre.apsevilla.com/v2/entities?limit=100&offset=0&options=count&idPattern=.*&q=category%3D%3DmarinerNotice&type=Alert",
    "bridges": "https://context-pre.apsevilla.com/v2/entities?limit=100&offset=0&options=count&idPattern=.*&type=Bridge&orderBy=!dateIssued",
    "terminals": "https://context-pre.apsevilla.com/v2/entities?type=Terminal",
    "floodgates": "https://context-pre.apsevilla.com/v2/entities?type=Floodgate",
    "ports": "https://context-pre.apsevilla.com/v2/entities?type=Port",
    "sea_conditions": "https://context-pre.apsevilla.com/v2/entities?limit=100&offset=0&options=count&idPattern=.*&type=SeaConditionsObserved&orderBy=!dateIssued",
    "vessels": "https://context-pre.apsevilla.com/v2/entities?limit=1000&type=Vessel",
    "canal_status": "https://context-pre.apsevilla.com/v2/entities?type=CanalStatusObserved",
    "harvester_config": "https://context-pre.apsevilla.com/v2/entities?type=HarvesterConfig",
    "sea_conditions_forecast": "https://context-pre.apsevilla.com/v2/entities?type=SeaConditionsForecast",
    "weather_forecast": "https://context-pre.apsevilla.com/v2/entities?type=WeatherForecast"
}

def fetch_and_clean(url):
    response = requests.get(url, verify=False)
    response.raise_for_status()
    data = response.json()

    cleaned_data = []
    for entity in data:
        cleaned_data.append(clean_entity(entity))
    return cleaned_data

def clean_entity(entity):
    new_entity = entity.copy()

    location = entity.get('location', {}).get('value', {})
    coordinates = location.get('coordinates')
    location_type = location.get('type')

    if coordinates:
        if location_type == 'Point':
            new_entity['longitude'] = coordinates[0]
            new_entity['latitude'] = coordinates[1]
        elif location_type == 'Polygon':
            first_point = coordinates[0][0]
            new_entity['longitude'] = first_point[0]
            new_entity['latitude'] = first_point[1]

    new_entity.pop('location', None)
    return new_entity

# Crear las rutas de manera correcta
for name, url in URLS.items():
    def make_proxy(url):
        def proxy():
            return jsonify(fetch_and_clean(url))
        return proxy

    app.add_url_rule(f"/proxy_{name}", view_func=make_proxy(url), endpoint=name)

# Ruta para obtener todo
@app.route('/proxy_all')
def fetch_all_combined():
    all_data = []
    for name, url in URLS.items():
        try:
            cleaned = fetch_and_clean(url)
            all_data.extend(cleaned)
        except Exception as e:
            print(f"Error fetching {name}: {e}")
    return jsonify(all_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
