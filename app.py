#!/usr/bin/env python
import requests, os, uuid, json
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, request, render_template, session
load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def index_post():
    # Read form values
    original_text = request.form["text"]
    target_language = request.form["language"]

    # Load .env values
    key = os.environ["KEY"]
    endpoint = os.environ["ENDPOINT"]
    location = os.environ["LOCATION"]

    # Path to the translation API version
    path = "/translate?api-version=3.0"

    # Add the parameter for the target language
    target_lang_param = "&to=" + target_language

    # Create the URL
    final_url = endpoint + path + target_lang_param

    # Set up the header info, including subscription key
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": location,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4())
    }

    # Create the request body of text to translate
    body = [{ "text": original_text}]

    # Make the call using POST
    translator_request = requests.post(final_url, headers=headers, json=body)

    # Retrieve JSON response
    translator_response = translator_request.json()

    # Retrieve translated text
    translated_text = translator_response[0]["translation"][0]["text"]

    # Call render template and pass in the translated text
    # plus the original text and target language
    return render_template("results.html",
                           translated_text=translated_text,
                           original_text=original_text,
                           target_language=target_language
                           )
