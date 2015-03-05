from flask import Flask, render_template, url_for, request, jsonify
#from main import *
from printform import *
import json
app = Flask(__name__)
# @app.route('/')
# def hello_world():
	# return "Hello world!"
@app.route('/')
def renderTest():
	return render_template("test.html")
	
@app.route('/load_ajax', methods = ["GET", "POST"])
def load_ajax():
	#data = request.args.get(data)
	#board file
	brdfile = request.args.get("BRDF")
	#net to analyze
	net2analyze = request.args.get("NET2A")
	#vrm
	vrm = request.args.get("VRM")
	#sink
	sink = request.args.get("SINKC")
	#vrm inductor
	vrml = request.args.get("VRML")
	#What machine to run?
	
	#Project?
	
	printform(brdfile, net2analyze, vrm, sink, vrml)
	#main()
	# return jsonify(result = brdfile), jsonify(result=net2analyze), jsonify(result=vrm), jsonify(result=sink), jsonify(result=vrml)
	#return jsonify(result=brdfile)
	return console.log('success')
if __name__ == "__main__":
	app.run(host='0.0.0.0')
	

