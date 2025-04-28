from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

# Ruta general que reenviará todas las peticiones
@app.route('/proxy')
def proxy_request():
    target_url = request.args.get('target')
    if not target_url:
        return {"error": "Missing 'target' query parameter"}, 400

    try:
        # Petición ignorando certificados SSL
        response = requests.get(target_url, verify=False)
        response.raise_for_status()
        data = response.json()

        return jsonify(data)
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
