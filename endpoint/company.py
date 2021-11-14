from app import app
from utilities import dbconn
from flask import request, Response
import json
import mariadb


@app.route("/api/company", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def company():
    conn = None
    cursor = None
    (conn, cursor) = dbconn()
    
    if request.method == 'GET':
        params = request.args
        token = request.headers.get('token')
        try:
            cursor.execute('SELECT user_id, role FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE login_token = ?', [token,])
            result = cursor.fetchone()
            
            if result[1] == 'admin':
                cursor.execute('SELECT company_name, phone, address, city, region, country, zip_postal, date_active FROM company')
                result = cursor.fetchall()
                companyArray = []
                for company in result:
                    companyDict = {
                        'companyName' : company[0],
                        'phone' : company[1],
                        'address' : company[2],
                        'city' : company[3],
                        'region' : company[4],
                        'country' : company[5],
                        'zip_postal' : company[6],
                        'date_active' : company[7]
                    }
                    companyArray.append(companyDict)
                    print(companyDict)
                
                return Response(json.dumps(companyArray, default=str),
                                mimetype='application/json',
                                status=200)
            else:
                return Response(json.dumps("There was an error accessing the information",
                                            mimetype= 'application/json',
                                            status=403))
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
        token = request.headers.get('token')
        try:
            cursor.execute('SELECT role FROM user INNER JOIN user_session ON user.id = user_session.user_id')
            result = cursor.fetchall()
            if result[0] == ('admin',):
                cursor.execute('INSERT INTO company (company_name, phone, address, city, region, country, zip_postal, date_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                                [request.json.get('company'),
                                request.json.get('phoneNumber'),
                                request.json.get('address'),
                                request.json.get('city'),
                                request.json.get('region'),
                                request.json.get('country'),
                                request.json.get('zip'),
                                request.json.get('activeDate')])
                conn.commit()

                return Response(status=201)
            else:
                return Response("You are not authorized to complete this action",
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
    
    elif request.method == 'PATCH':
        token = request.headers.get('token')
        try:
            cursor.execute('SELECT user_id, role FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE login_token = ?', [token,])
            result = cursor.fetchone()
            if result[1] == ('admin'):
                companyId = request.json.get('id')
                if request.json.get('company_name') != None:
                    cursor.execute('UPDATE company SET company_name = ? WHERE company.id = ?', [request.json.get('company_name'), companyId,])
                else:
                    pass
                if request.json.get('phone') != None:
                    cursor.execute('UPDATE company SET phone = ? WHERE company.id = ?', [request.json.get('phone'), companyId,])
                else:
                    pass
                if request.json.get('address') != None:
                    cursor.execute('UPDATE company SET address = ? WHERE company.id = ?', [request.json.get('address'), companyId,])
                else:
                    pass
                if request.json.get('city') != None:
                    cursor.execute('UPDATE company SET city = ? WHERE company.id = ?', [request.json.get('city'), companyId,])
                else:
                    pass
                if request.json.get('region') != None:
                    cursor.execute('UPDATE company SET region = ? WHERE company.id = ?', [request.json.get('region'), companyId,])
                else:
                    pass
                if request.json.get('country') !=None:
                    cursor.execute('UPDATE company SET country = ? WHERE company.id = ?', [request.json.get('country'), companyId,])
                else:
                    pass
                if request.json.get('zip_postal') != None:
                    cursor.execute('UPDATE company SET zip_postal = ? WHERE company.id = ?', [request.json.get('zip_postal'), companyId,])
                else:
                    pass
                cursor.execute('SELECT * FROM company WHERE company.id = ?', [companyId,])
                updateCompany = cursor.fetchall()
                updated = []
                for company in updateCompany:
                    companyUpdate = {
                        'company_name' : company[1],
                        'phone' : company[2],
                        'address' : company[3],
                        'city' : company[4],
                        'region' : company[5],
                        'country' : company[6],
                        'zip_postal' : company[7]
                    }
                    updated.append(companyUpdate)
                conn.commit()

                return Response(json.dumps(updated, default=str),
                                mimetype='application/json',
                                status=200)
            else:
                return Response(json.dumps("Failed to update"),
                                mimetype='application.json',
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
        companyId = request.json.get('id')
        try:
            cursor.execute('SELECT user_id, role FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE login_token = ?', [token,])
            result = cursor.fetchone()
            if result[1] == ('admin'):
                cursor.execute('SELECT * FROM company WHERE company.id = ?', [companyId,])
                result = cursor.fetchall()
                if cursor.rowcount == 1:
                    cursor.execute('DELETE FROM company WHERE company.id = ?', [companyId,])
                    conn.commit()

                    return Response(json.dumps("Delete successful"),
                                    mimetype='application/json',
                                    status=200)
                else:
                    return Response(json.dumps("Request cannot be completed"),
                                    mimetype='application/json',
                                    status=403)
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