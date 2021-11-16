from app import app
from utilities import dbconn
from flask import request, Response
import json
import mariadb
import bcrypt



@app.route("/api/user", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def user():
    conn = None
    cursor = None
    (conn, cursor) = dbconn()

    if request.method == 'GET':
        params = request.args
        # userId = params.get('userId')
        token = request.headers.get('token')
        try:
            cursor.execute('SELECT user_id, role FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE login_token = ?', [token,])
            result = cursor.fetchone()
            if result[1] == 'admin':
                cursor.execute('SELECT email, role, created_at, first_name, last_name, user.id, company_name FROM user INNER JOIN company on user.company_id = company.id')
                result = cursor.fetchall()
                print(result)
                userArray = []
                for user in result:
                    userDict = {
                        'fName' : user[3],
                        'lName' : user[4],
                        'email' : user[0],
                        'role' : user[1],
                        'companyName' : user[6],
                        'created' : user[2],
                        'userId' : user[5]    
                    }
                    userArray.append(userDict)
                return Response(json.dumps(userArray, default=str),
                                mimetype='application/json',
                                status=200)
                
            else:
                return Response(json.dumps("error", default=str),
                            mimetype='application/json',
                            status=400)
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
    
    elif request.method == 'POST':
        try:
            cursor.execute('SELECT role FROM user INNER JOIN user_session ON user.id = user_session.user_id')
            result = cursor.fetchall()
            if result[0] == ('admin',):
                companyName = request.json.get('companyName')
                cursor.execute('SELECT id FROM company WHERE company_name = ?',[companyName,])
                companyMatch = cursor.fetchone()
                company = companyMatch[0]
                pwrd = request.json.get('password')
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(pwrd.encode(), salt)
                cursor.execute("INSERT INTO user (email, password, role, first_name, last_name, company_id) VALUES (?, ?, ?, ?, ?, ?)",
                                [request.json.get('email'),
                                hashed,
                                request.json.get('role'),
                                request.json.get('fName'),
                                request.json.get('lName'),
                                company])
                conn.commit()
                cursor.close()
                conn.close()
                return Response(status=201)
            else:
                return Response("You are not authorized to complete this action",
                                mimetype='text/plain',
                                status=400)
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


    elif request.method == 'PATCH':
        token = request.headers.get('token')
        try:
            cursor.execute('SELECT user_id, role FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE login_token = ?', [token,])
            result = cursor.fetchone()
            if result[1] == ('admin'):
                userId = request.json.get('userId')
                if request.json.get('fName') != None:
                    cursor.execute('UPDATE user SET first_name = ? WHERE user.id = ?',[request.json.get('fName'), userId,])
                else:
                    pass
                if request.json.get('lName') != None:
                    cursor.execute('UPDATE user SET last_name = ? WHERE user.id = ?', [request.json.get('lName'), userId,])
                else:
                    pass
                if request.json.get('email') != None:
                    cursor.execute('UPDATE user SET email = ? WHERE user.id = ?', [request.json.get('email'), userId])
                else:
                    pass
                if request.json.get('password') != None:
                    cursor.execute('UPDATE user SET password = ? WHERE user.id = ?', [request.json.get('password'), userId])
                else:
                    pass
                cursor.execute('SELECT first_name, last_name, email, role FROM user WHERE user.id = ?', [userId,])
                updateInfo = cursor.fetchall()
                update = []
                for user in updateInfo:
                    userUpdate = {
                        'first_name' : user[0],
                        'last_name' : user[1],
                        'email' : user[2],
                        'role' : user[3]
                    }
                    update.append(userUpdate)
                conn.commit()
                cursor.close()
                conn.close()
                return Response(json.dumps(userUpdate, default=str),
                                mimetype='application/json',
                                status=200)
            else:
                return Response(json.dumps('Failed to update'),
                                mimetype='application/json',
                                status=400)
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
    
    elif request.method == 'DELETE':
        token = request.headers.get('token')
        userId = request.json.get('userId')
        try:
            cursor.execute('SELECT user_id, role FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE login_token = ?', [token,])
            result = cursor.fetchone()
            if result[1] == ('admin'):
                cursor.execute('SELECT * FROM user WHERE user.id = ?', [userId,])
                result = cursor.fetchall()
                if cursor.rowcount == 1:
                    cursor.execute('DELETE FROM user WHERE user.id = ?', [userId,])
                    conn.commit()
                    cursor.close()
                    conn.close()
                    return Response(status=200)
                else:
                    return Response(json.dumps("Request cannot be completed"),
                                    mimetype='application/json',
                                    status=400)
            else:
                return Response(json.dumps("Authorization denied"),
                                mimetype='application/json',
                                status=403)
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
