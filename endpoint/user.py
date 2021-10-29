from app import app
from utilities import dbconn
from flask import request, Response
import json


@app.route("/api/user", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def user():
    conn = None
    cursor = None
    (conn, cursor) = dbconn()
    if request.method == 'GET':
        params = request.args
        pass
    
    elif request.method == 'POST':
        cursor.execute('SELECT role FROM user INNER JOIN user_session ON user.id = user_session.user_id')
        result = cursor.fetchall()
        if result == [('super admin',)]:
            newUser = request.json.get('contact')
            cursor.execute("INSERT INTO user (email, password, role, company, address, phone, contact) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            [request.json.get('email'),
                            request.json.get('password'),
                            request.json.get('role'),
                            request.json.get('company'),
                            request.json.get('address'),
                            request.json.get('phone'),
                            request.json.get('contact')])
            return Response(json.dumps(newUser))
        else:
            return Response("You are not authorized to complete this action",
                            mimetype='text/plain',
                            status=400)
