from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


@app.route('/api/pinfo', methods=['POST'])
def get_pinfo():
    data = request.get_json(force=True, silent=True)
    if not data or 'pid' not in data:
        return jsonify({"error": "No PID provided"}), 400

    pid = data.get('pid')
    url = "http://rwfc.net/api/pinfo"

    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json={"pid": pid}, headers=headers, timeout=10)

        if response.status_code != 200:
            return jsonify({
                "error": f"Upstream API returned {response.status_code}",
                "content": response.text[:100]
            }), response.status_code

        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3008)