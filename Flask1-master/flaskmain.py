from flask import Flask, render_template, url_for, request
import json
app = Flask(__name__, template_folder='templates', static_folder="static")

@app.route('/')
def rendermain():
    return render_template('index.html')

@app.route('/calculateSum')
def calculateSum():
    num1 = int(request.args.get('num1'))
    num2 = int(request.args.get('num2'))
    print "num1 = %d, num2 = %d" % (num1, num2)
    return json.dumps({"result": num1 + num2}) 
#def hello_world():
#    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)
