import os
import requests
import json

from flask import Flask, session, request, render_template, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import numpy as np

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)