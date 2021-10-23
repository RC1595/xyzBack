from app import app
from utilities import dbconn
from flask import request, Response
import json


@app.route("/api/user", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def user():
    conn = None
    cursor = None
    (conn, cursor) = dbconn()
    