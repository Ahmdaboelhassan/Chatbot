from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from chatbot_response import chatbot_response
from waitress import serve

# Model Names
General = "General"
Depression = "Depression"
Anxiety = "Anxiety"
Stress = "Stress"
SleepDisorder = "SleepDisorder"
Phobia = "Phobia"
PersonaltyDisorder = "PersonaltyDisorder"

# Array of Names
app_models = [Depression, Anxiety, Stress, SleepDisorder, Phobia, PersonaltyDisorder]

# Key Strings
ClearKeyMsgs = ["forget-memory", "clear-memory", "forget-model", "clear-model"]
CookieKey = "SelectedModel"

app = Flask(__name__)
cors = CORS(app)

# helping method
def server_response(msg, model_name=General):
    result = chatbot_response(msg, model_name)
    response = make_response(jsonify({'answer': result}))
    response.set_cookie(CookieKey, model_name, max_age=1800)
    return response


# http://localhost:5000/ChatBot?msg=""
@app.route('/ChatBot/', methods=['GET'])
def chatbot():
    model_from_cookie = request.cookies.get(CookieKey)
    msg = request.args.get('msg')

    if msg in ClearKeyMsgs:
        response = make_response(jsonify({'answer': "Memory Cleared Successfully"}))
        response.set_cookie(CookieKey, General, max_age=180)
        return response

    if model_from_cookie is None or model_from_cookie not in app_models:
        result = chatbot_response(msg)
        if result in app_models:
            return server_response(msg, result)
        return server_response(msg)

    return server_response(msg, model_from_cookie)


# http://localhost:5000/ChatBot/Disease?name=""
@app.route('/ChatBot/Disease', methods=['GET'])
def chatbot_disease():
    disease_name = request.args.get('name')

    if (disease_name is not None) and (disease_name in app_models):
        res = make_response(jsonify({'answer': f"Tell me what you want to Know About {disease_name}"}))
        res.set_cookie(CookieKey, disease_name)
        return res

    return jsonify({'answer': f"I Don't have knowledge About {disease_name} yet"})

def run_server():
    # if __name__ == '__main__':
        # app.run()
        serve(app, port=5000)

run_server()
