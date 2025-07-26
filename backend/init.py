from flask import Flask
from flask_cors import CORS
from init import *

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": "http://localhost:5173",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

CORS(app, supports_credentials=True) 
