from flask import Flask, render_template, request, jsonify
import json
import random

import pyttsx3

import os
from gtts import gTTS
import time

app = Flask(__name__)

# Load tags and responses from the JSON file
with open('responses.json', 'r') as file:
    responses_data = json.load(file)
    tags_and_responses = responses_data.get('tags', [])

def get_response(user_input):
    print(f"User Input: {user_input}")

    for tag_data in tags_and_responses:
        if tag_data["tag"] in user_input.lower():
            selected_response = random.choice(tag_data["responses"])
            print(f"Selected Response: {selected_response}")
            return selected_response

    # If no matching tag is found, use the default tag
    default_responses = next((tag["responses"] for tag in tags_and_responses if tag["tag"] == "default"), [])
    print(f"Default Responses: {default_responses}")
    return random.choice(default_responses)


@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    input_message = msg

    # Call the function to generate a response
    response = get_response(input_message)

    voice_path = generate_voice_response(response)

    return jsonify({'text_response': response, 'voice_response': voice_path})

def generate_voice_response(text_response):
    timestamp = int(time.time())
    voice_path = f'static/voice_response_{timestamp}.mp3'
    voice_response = gTTS(text=text_response, lang='en', slow=False)
    voice_response.save(voice_path)

    # Play the audio response

    engine = pyttsx3.init()
    engine.say(text_response)
    engine.runAndWait()
    engine.stop()

    # Delete the audio file after playing
    os.remove(voice_path)

    return voice_path

if __name__ == '__main__':
    app.run(debug=True)
