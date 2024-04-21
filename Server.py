from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from chatbot_response import chatbot_response
from waitress import serve


app = Flask(__name__)
cors = CORS(app)

# http://localhost:5000/ChatBot?msg=""
@app.route('/ChatBot/', methods=['GET','POST'])
def chatbot():
    try:
        if request.method == "GET":
            msg = request.args.get('msg')

        elif request.method == "POST":
            body = request.json
            msg = body["msg"]
    except:
        return jsonify({'answer': "An ERROR OCCURED"}) , 400
    
    if len(msg) < 2 :
         return jsonify({'answer': "Please Send Valid Msg"}) , 400
    
    answer = chatbot_response(msg)
    return jsonify({'answer': answer}) , 200



def run_server():
    # if __name__ == '__main__':
        # app.run()
        serve(app, port=5000)

run_server()
