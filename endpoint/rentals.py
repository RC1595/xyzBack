from app import app
from utilities import dbconn
from flask import request, Response
import json
import mariadb



@app.route("/api/rentals", methods=['GET', 'POST', 'PATCH'])
def rentals():
    conn = None
    cursor = None
    (conn, cursor) = dbconn()
    token = request.headers.get('token')
    
    if request.method == 'GET':
        params = request.args
        cursor.execute('SELECT user_id, role FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE login_token = ?', [token,])
        result = cursor.fetchone()
        if result[1] == ('admin'):
            try:
                cursor.execute('SELECT rentals.serial_number, date_out, date_in, company_name, phone, first_name, last_name, email FROM rentals INNER JOIN equipment ON rentals.serial_number = equipment.serial_number INNER JOIN company ON rentals.company_id = company.id INNER JOIN user ON rentals.user_id = user.id')
                result = cursor.fetchall()
                rentalArray = []
                for rental in result:
                    rentalDict ={
                        'sn' : rental[0],
                        'dateOut' : rental[1],
                        'dateIn' : rental[2],
                        'companyName' : rental[3],
                        'phone' : rental[4],
                        'fName' : rental[5],
                        'lName' : rental[6],
                        'email' : rental[7]
                    }
                    rentalArray.append(rentalDict)
                return Response(json.dumps(rentalArray, default=str),
                                mimetype= 'application/json',
                                status= 200)
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
                
        else:
            return Response(json.dumps("error processing your request"),
                            mimetype='application/json',
                            status= 400)
        
    
    elif request.method == 'POST':
        sn = request.json.get('selectedSn')
        cursor.execute('SELECT user_id, role FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE login_token = ?', [token,])
        result = cursor.fetchone()
        if result[1] == ('admin'):
            cursor.execute('SELECT serial_number from equipment WHERE serial_number = ?', [sn,])
            cursor.fetchall()
            if cursor.rowcount == 1:
                try:
                    cursor.execute('UPDATE equipment SET in_stock = ? WHERE serial_number = ?', [1, sn,])
                    cursor.execute('INSERT INTO rentals (serial_number, company_id, user_id) VALUES (?, ?, ?)', [
                        sn, 
                        request.json.get('selectedCompany'),
                        request.json.get('selectedUser'),])
                    conn.commit()
                    return Response(status=201)
                
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
            else:
                return Response(status=401)
        else: 
            return Response(status=400)
        
    elif request.method == 'PATCH':
        cursor.execute('SELECT user_id, role FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE login_token = ?', [token,])
        result = cursor.fetchone()
        if result[1] == ('admin'):
            sn = request.json.get('sn')
            try:
                if request.json.get('dateIn') != None:
                    cursor.execute('UPDATE rentals SET date_in = ? WHERE serial_number = ?', [request.json.get('dateIn'), sn,])
                    conn.commit()
                    cursor.execute('UPDATE equipment SET in_stock = ? WHERE serial_number = ?', [0, sn,])
                    conn.commit()
                else:
                    pass
                return Response(status=200)

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
        else:
            return Response(status=401)
