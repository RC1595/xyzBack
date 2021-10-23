from app import app
from flask import request, Response
import json
import mariadb
from uuid import uuid4
from utilities import dbconn, login



@app.route("/api/login", methods=['POST', 'DELETE'])
def credcheck():
    try:
        conn = None
        cursor = None
        (conn, cursor) = dbconn()
        if request.method == 'POST':
            email = request.json.get('email')
            pwrd = request.json.get('password')
            cursor.execute('SELECT * from user WHERE email =? AND password = ?', [email, pwrd])
            result = cursor.fetchall()
            if (cursor.rowcount == 1):
                if pwrd == result[0][2]:
                    userId = result[0][0]
                    loginToken = login(userId)
                    loginDict = {
                        "userId" : userId,
                        "loginToken" : loginToken
                    }
                    conn.commit()
                    cursor.close()
                    conn.close()
                    return Response(json.dumps(loginDict),
                                mimetype='application/json',
                                status=200)
                else: 
                    return Response("Your email and password do not match",
                                mimetype='text/plain',
                                status=401)
            else:
                return Response("Something went wrong",
                                mimetype='text/plain',
                                status=401)
        elif request.method == 'DELETE':
            token = request.json.get('loginToken')
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
    # finally:
    #     if (cursor != None):
    #         cursor.close()
    #     if (conn != None):
    #         conn.close()