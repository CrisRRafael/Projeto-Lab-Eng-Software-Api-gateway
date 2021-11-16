from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
from urllib import parse, request as req


app = Flask(__name__)
CORS(app)

calculations_service= {'operation':'/calculate', 'address':'localhost', 'port':5001, 'route':'/calculate'}
list_logs = {'operation':'/logs', 'address':'localhost', 'port':5003, 'route': "/logs"}
create_log = {'operation':'/create-log', 'address':'localhost', 'port':5003, 'route': "/create-log"}
calc_espe_service= {'operation':'/calc_raiz', 'address':'localhost', 'port':5004, 'route':'/calc_raiz'}

service_registry = [calculations_service, create_log, list_logs, calc_espe_service]

@app.route('/api_gateway/<operation>', methods=['POST', 'GET'])
def api_gateway(operation):
    for service_config in service_registry:
        if service_config['operation'] == ('/'+operation):
            
            parameters = { 'str_input': request.args.get('str_input')}
            url = 'http://' + service_config['address'] +':' + str(service_config['port']) + service_config['route'] 
            url_request = req.urlopen(url+'?'+parse.urlencode(parameters))
            result = url_request.read()
            
            return result

if __name__ == "__main__":
    app.run(port=5002)

