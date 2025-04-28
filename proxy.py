from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/entities')
def get_entities():
    url = 'https://context-pre.apsevilla.com/v2/entities'
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))  # Leer puerto de variable de entorno
    app.run(host='0.0.0.0', port=port)        # Escuchar en 0.0.0.0
