from flask import Flask, render_template, request, stream_with_context, Response
from lib.lib_gemini import streamGem
from lib.lib_openai import streamGPT

import os
from dotenv import load_dotenv
load_dotenv()

port = 5000

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        c_user = request.form.get('c_user').lower()
        if c_user == os.getenv("APP_ACCESS"):
            return render_template('index.html')
    return render_template('login.html')

@app.route("/process", methods = ["POST"])
def _process():
    json_data = request.get_json()
    seva = json_data['seva']
    if seva == 0:
        return streamGPT(json_data), {"Content-type": "text/plain"}
    elif seva == 1:
        return streamGem(json_data), {"Content-type": "text/plain"}

    return "Unknown model!"

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = port, debug = False)
