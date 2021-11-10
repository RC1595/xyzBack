from app import app
from flask import request, Response
import json
import mariadb
from uuid import uuid4
from utilities import dbconn
import bcrypt




@app.route("/api/login", methods=['POST', 'DELETE'])
def credcheck():
    try:
        conn = None
        cursor = None
        (conn, cursor) = dbconn() 
        if request.method == 'POST':
            email = request.json.get('email')
            while True:
                pw_in = request.json.get('password')
                cursor.execute ('SELECT password, id from user WHERE email = ?', [email,])
                result = cursor.fetchone()
                if result == None:
                    return Response("That user does not exist",
                                    mimetype='text/plain',
                                    status=403)
                pw_db = result[0] 
                user_id = result[1]
                
                if (bcrypt.checkpw(pw_in.encode(), pw_db.encode())): 
                    print("match")
                    loginToken = newToken(user_id)
                    loginDict = {
                        "userId" : user_id,
                        "loginToken" : loginToken
                        }
                    cursor.close()
                    conn.close()
                    return Response(json.dumps(loginDict),
                                    mimetype='application/json',
                                    status=200)
                else: 
                    return Response("Your email and password do not match",
                                        mimetype='text/plain',
                                        status=403)

        elif request.method == 'DELETE':
            token = request.json.get('token')
            cursor.execute('SELECT * from user_session WHERE login_token = ?', [token,])
            result = cursor.fetchall()
            if (cursor.rowcount == 1):
                cursor.execute('DELETE from user_session WHERE login_token = ?', [token,])
                conn.commit()
                cursor.close()
                conn.close()
                return Response(
                                mimetype='application.json',
                                status=204)
            else:
                return Response("Could not sign out")
            
    except ConnectionError:
        return Response ("There was a problem connecting to the database",
                        mimetype= 'text/plain',
                        status= 400)
    except mariadb.DataError:
        return Response ("There was a problem processing your request",
                        mimetype= 'text/plain',
                        status= 400)
    except mariadb.OperationalError:
        return Response ("Operational error on connection",
                        mimetype='text/plain',
                        status= 400)
    except mariadb.ProgrammingError:
        return Response ("Bad query",
                        mimetype='text/plain',
                        status= 400)
    except mariadb.IntegrityError:
        return Response ("Harmful query detected",
                        mimetype= 'text/plain',
                        status= 403)
    finally:
        if (cursor != None):
            cursor.close()
        if (conn != None):
            conn.close()
    
def newToken(userId):
    loginToken = uuid4().hex
    (conn, cursor) = dbconn()
    cursor.execute('INSERT INTO user_session (login_token, user_id) VALUES (?, ?)', [loginToken, userId])
    conn.commit()
    cursor.close()
    conn.close()
    return loginToken