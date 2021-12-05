from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
from urllib import parse, request as req
import requests

app = Flask(__name__)
CORS(app)

calculations_service= {'operation':'/calculate', 'address':'192.168.15.9', 'port':'5001', 'route':'/calculate'}
list_logs = {'operation':'/logs', 'address':'localhost', 'port':'5003', 'route': "/logs"}
create_log = {'operation':'/create-log', 'address':'localhost', 'port':'5003', 'route': "/create-log"}
calc_espe_service= {'operation':'/calc_raiz', 'address':'192.168.15.9', 'port':'5004', 'route':'/calc_raiz'}

service_registry = {'calculate': calculations_service, 'calc_raiz': calc_espe_service, 'logs': list_logs, "create-log": create_log}

@app.route('/api_gateway/<operation>', methods=['POST', 'GET'])
def api_gateway(operation):
  response = ""
  json_request = request.form

  service = service_registry[operation]
  url = 'http://' +  service['address'] + ':' + service['port'] + service['route']

  if json_request:
    response = requests.post(url, json=json_request)
    form_read = request.form
            
    d = form_read['date']
    ds = d.split(' ')

    body = {
        'operation': form_read['operation'],
        'argument': form_read['argument'],
        'type_operation': form_read['type_operation'],
        'date': ds[2] + '/' + '12' + '/' + ds[3],
    }

    qstring = parse.urlencode(body)
    url_query = req.urlopen(url, qstring.encode('ascii'))
    resp = url_query.read()

    return resp

  else:

    parameters = request.args.get('str_input')

    if (parameters): 
        response = requests.get(url+'?str_input='+parameters)
    
        print(url)
    
    else:
        response = requests.get(url)

  return { 'data': response.json() }

if __name__ == "__main__":
    app.run(port=5002)

