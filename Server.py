from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from chatbot_response import chatbot_response
from waitress import serve
import speech_recognition as sr
import assemblyai as aai
from io import BytesIO


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

        audio_file = BytesIO(file.read())

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file)
        
        text = transcript.text

        print("The Text In Audio Is => ", text)       

        answer = chatbot_response(text)

        print("The Answer From Model => ", answer)       
        
        return jsonify({'answer': text}) , 200
    
    except Exception as ex:
        print("Expection => ", ex) 
        print("Expection From Audio => ", transcript.error) 

        return jsonify({'answer': "Something Wrong Happend"}) , 400
    
def run_server():
    # if __name__ == '__main__':
        print("Application Run Successfully.... :)")
        # app.run()
        serve(app, port=5000)

run_server()

