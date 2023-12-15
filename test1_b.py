from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from flask_cors import CORS  

app = Flask(__name__)
es = Elasticsearch()
CORS(app) 

# Endpoint to insert payload into Elasticsearch
@app.route('/add', methods=['POST'])
def add_to_elasticsearch():
    try:
        # JSON file path is passed as a parameter
        json_file_path = request.args.get('json_file_path')

        if not json_file_path:
            return jsonify({"status": "error", "message": "Missing path parameter"}), 400

        with open(json_file_path, 'r') as file:
            json_data = file.read()
        print(json_data)
        # Index the JSON data into Elasticsearch
        es.index(index='exampleindex', doc_type='_doc', body=json_data)

        return jsonify({"status": "success", "message": "Data added to Elasticsearch"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    if es.ping():
        return jsonify({"status": "UP"}), 200
    else:
        return jsonify({"status": "DOWN"}), 500
    
@app.route('/healthcheck/<service_name>', methods=['GET'])
def healthcheck_service(service_name):
    if es.ping():
        return jsonify({"service": service_name, "status": "UP"}), 200
    else:
        return jsonify({"service": service_name, "status": "DOWN"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
