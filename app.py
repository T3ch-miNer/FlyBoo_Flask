# /app.py
from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# run Flask app
if __name__ == "__main__":
    app.run()


#processing the request from dialogflow
def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:                    #match the intent
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response.query_result.fulfillment_text

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en') #maintain session
    response_text = { "message":  fulfillment_text }
    print(response_text)
    return jsonify(response_text)

