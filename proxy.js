from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/entities')
def get_entities():
    url = 'https://context-pre.apsevilla.com/v2/entities'
    try:
        response = requests.get(url, verify=False)  # Ignoramos problemas de SSL
        response.raise_for_status()  # Lanza error si la respuesta no es 200
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(port=3000)