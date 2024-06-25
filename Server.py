from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from chatbot_response import chatbot_response
from waitress import serve
import speech_recognition as sr

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
        return jsonify({'answer': "An ERROR OCCURED"}) , 200
    
    answer = chatbot_response(msg)
    print(msg)
    return jsonify({'answer': answer}) , 200

@app.route("/ChatBot/Record", methods=["POST"])
def Chatbot_Record():
    transcript = ""
    if "Record" not in request.files:
        return jsonify({'answer': "Please Send Record" }) , 200

    file = request.files["Record"]
    if file.filename == "":
        return jsonify({'answer': "Record was not sent" }) , 200
# try :
    if file:
        recognizer = sr.Recognizer()
        audioFile = sr.AudioFile(file)
        with audioFile as source:
            data = recognizer.record(source)
            transcript = recognizer.recognize_google(data)
    print('#'*80)       
    answer = chatbot_response(transcript)
    print('#'*80)       
    return jsonify({'answer': answer}) , 200
# except:
#     return jsonify({'answer': "Something Wrong Happend"}) , 200
    
def run_server():
    # if __name__ == '__main__':
        print("Application Run Successfully.... :)")
        # app.run()
        serve(app, port=5000)

run_server()

