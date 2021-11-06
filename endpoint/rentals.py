from app import app
from utilities import dbconn
from flask import request, Response
import json

@app.route("/api/rentals", methods=['GET', 'POST', 'PATCH'])
def equipment():
    conn = None
    cursor = None
    (conn, cursor) = dbconn()
    token = request.headers.get('token')
    
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'PATCH':
        pass