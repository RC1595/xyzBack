from app import app
from utilities import dbconn
from flask import request, Response
import json
import bcrypt


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
            newUser = request.json.get('first_name')
            pwrd = request.json.get('password')
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(pwrd.encode(), salt)
            cursor.execute("INSERT INTO user (email, password, role, company, address, phone, first_name, last_name, city, region, country, zip_postal, date_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )",
                            [request.json.get('email'),
                            hashed,
                            request.json.get('role'),
                            request.json.get('companyName'),
                            request.json.get('address'),
                            request.json.get('phoneNumber'),
                            request.json.get('fName'),
                            request.json.get('lName'),
                            request.json.get('city'),
                            request.json.get('region'),
                            request.json.get('country'),
                            request.json.get('zip'),
                            request.json.get('activeDate')])
            conn.commit()
            cursor.close()
            conn.close()
            return Response(json.dumps(newUser))
        else:
            return Response("You are not authorized to complete this action",
                            mimetype='text/plain',
                            status=400)
