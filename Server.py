from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from chatbot_response import chatbot_response
from waitress import serve
import speech_recognition as sr
import os
import time
import assemblyai as aai


app = Flask(__name__)
cors = CORS(app)
aai.settings.api_key = "6ced9089260548e79c6ede9ff7852c20"

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
        return jsonify({'answer': "An ERROR OCCURED"}) , 200
    
    answer = chatbot_response(msg)
    print(msg)
    return jsonify({'answer': answer}) , 200

@app.route("/ChatBot/Record", methods=["POST"])
def Chatbot_Record():
    if "Record" not in request.files:
        return jsonify({'answer': "Please Send Record" }) , 400

    file = request.files["Record"]
    if file.filename == "":
        return jsonify({'answer': "Record was not sent" }) , 400
    
    try :

        filename = str(int(round(time.time() * 1000))) + ".wav"
        cwd = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(cwd,"Records", filename)
        file.save(path)
        print("The File Has Been Saved Correctly")

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(path)
        print("The Text In Audio Is => ", transcript.text)       

        answer = chatbot_response(transcript.text)

        print("The Answer Sound => ",answer)       

        os.remove(path)
        return jsonify({'answer': answer}) , 200
    except Exception as ex:
        print("Expection => ", ex) 
        return jsonify({'answer': "Something Wrong Happend"}) , 400
    
def run_server():
    # if __name__ == '__main__':
        print("Application Run Successfully.... :)")
        # app.run()
        serve(app, port=5000)

run_server()

