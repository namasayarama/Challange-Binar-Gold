#flask API, Swagger UI

from cgitb import text
import sqlite3
from crypt import methods
from operator import sub
import pandas as pd
import re
import json

from text_cleaning_helper import *
from flask import request, Flask, jsonify
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app = Flask(__name__)

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title': LazyString(lambda:'API Documentation for Data Processing and Modeling'),
        'version': LazyString(lambda:'1.0.0'),
        'description': LazyString(lambda:'Dokumentasi API untuk Data Processing dan Modeling')
        }, host = LazyString(lambda: request.host)
    )

swagger_config = {
        "headers":[],
        "specs":[
            {
            "endpoint":'docs',
            "route":'/docs.json'
            }
        ],
        "static_url_path":"/flasgger_static",
        "swagger_ui":True,
        "specs_route":"/docs/"
    }

swagger = Swagger(app, template=swagger_template, config=swagger_config)
@swag_from("docs/hello_world.yml", methods=['GET'])
@app.route('/', methods=['GET'])
def hello_world():
    json_response = { 
        'status_code':200, 
        'description':'Successful response', 
        'status_code': 400,
        'description':'Bad Request', 
        'status_code': 500,
        'description':'Internal Server Error', 
        'data': "Hello World"
        }
    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text_processing', methods=['POST'])
def text_processing():
    text = str (request.form.get('text'))
    json_response = { 
        'status_code':200, 
        'description':'Successful response', 
        'data': re.sub('[^0-9a-zA-Z]+', ' ', text),
        }
    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/text_processing_file.yml", methods=['POST'])
@app.route('/text_processing_file', methods=['POST'])
def text_processing_file():
    text = request.form.get('file')[0]

    abusive_dictionery = pd.read_csv("docs/abusive.csv")
    df_alay = pd.read_csv("docs/new_kamusalay.csv")
    alay_dict = df_alay. rename (columns = {0: 'original', 1: 'replacement'})
   
    json_response = { 
        'status_code':200, 
        'description':'Successful response', 
        'data': 'success'
        }
    response_data = jsonify(json_response)
    return response_data


if __name__ == '__main__':
	app.run()