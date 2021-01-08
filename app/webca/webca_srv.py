#!/usr/bin/python3

#-Load required base modules---------------------------------------
import os
import sys
import json
import importlib

from flask import Flask, request, session, send_from_directory

#-Load required custom modules-------------------------------------
from classes import helpers

#------------------------------------------------------------------


#-Global Vars------------------------------------------------------
CurPath = os.path.dirname(os.path.realpath(__file__))
myHelper = helpers.helpers()


#-Build the flask app object---------------------------------------
app = Flask(__name__, static_url_path='', static_folder='content',)
app.secret_key = "changeit"
app.debug = True






#-The API Request Handler Area-------------------------------------
@app.route('/api', methods=['GET'])
def hello_app():
  myHelper.hello_world()
  
  return 'Hello from the WebCA API!'




#-The static web content serve-------------------------------------
@app.route('/')
def root():
  return app.send_static_file('index.html')





#-App Runner------------------------------------------------------
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)

#------------------------------------------------------------------