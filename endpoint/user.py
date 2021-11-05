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
        userId = params.get('userId')
        token = request.headers.get('token')

        cursor.execute('SELECT user_id, role FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE login_token = ?', [token,])
        result = cursor.fetchone()
        print(result)
        
        if result[1] == 'admin':
            cursor.execute('SELECT email, role, company_id, created_at, first_name, last_name FROM user')
            result = cursor.fetchall()
            userArray = []
            for user in result:
                userDict = {
                    'first_name' : user[4],
                    'last_name' : user[5],
                    'email' : user[0],
                    'role' : user[1],
                    'company_id' : user[2],
                    'created_at' : user[3]    
                }
                userArray.append(userDict)
            return Response(json.dumps(userArray, default=str),
                            mimetype='application/json',
                            status=200)
            
        


        else:
            return Response(json.dumps("error", default=str),
                        mimetype='application/json',
                        status=400)
    
    elif request.method == 'POST':
        cursor.execute('SELECT role FROM user INNER JOIN user_session ON user.id = user_session.user_id')
        result = cursor.fetchall()
        if result[0] == [('admin',)]:
            newUser = request.json.get('first_name')
            pwrd = request.json.get('password')
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(pwrd.encode(), salt)
            cursor.execute("INSERT INTO user (email, password, role, first_name, last_name) VALUES (?, ?, ?, ?, ?)",
                            [request.json.get('email'),
                            hashed,
                            request.json.get('role'),
                            request.json.get('fName'),
                            request.json.get('lName'),
])
            conn.commit()
            cursor.close()
            conn.close()
            return Response(json.dumps(newUser))
        else:
            return Response("You are not authorized to complete this action",
                            mimetype='text/plain',
                            status=400)
