from app import app
from utilities import dbconn
from flask import request, Response
import json



@app.route("/api/rentals", methods=['GET', 'POST', 'PATCH'])
def rentals():
    conn = None
    cursor = None
    (conn, cursor) = dbconn()
    token = request.headers.get('token')
    
    if request.method == 'GET':
        params = request.args
        cursor.execute('SELECT rentals.serial_number, date_out, date_in, company_name, phone, first_name, last_name, email FROM rentals INNER JOIN equipment ON rentals.serial_number = equipment.serial_number INNER JOIN company ON rentals.company_id = company.id INNER JOIN user ON rentals.user_id = user.id')
        result = cursor.fetchall()
        rentalArray = []
        for rental in result:
            rentalDict ={
                'serial_number' : rental[0],
                'date_out' : rental[1],
                'date_in' : rental[2],
                'company_name' : rental[3],
                'phone' : rental[4],
                'first_name' : rental[5],
                'last_name' : rental[6],
                'email' : rental[7]
            }
            rentalArray.append(rentalDict)
        return Response(json.dumps(rentalArray, default=str))
    
    elif request.method == 'POST':
        sn = request.json.get('sn')
        cursor.execute('SELECT user_id, role FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE login_token = ?', [token,])
        result = cursor.fetchone()
        if result[1] == ('admin'):
            cursor.execute('SELECT serial_number from equipment WHERE serial_number = ?', [sn,])
            cursor.fetchall()
            if cursor.rowcount == 1:
                try:
                    cursor.execute('UPDATE equipment SET in_stock = ? WHERE serial_number = ?', [1, sn,])
                    cursor.execute('INSERT INTO rentals (serial_number, company_id, user_id, date_in) VALUES (?, ?, ?, ?)', [
                        sn, 
                        request.json.get('company'),
                        request.json.get('userId'),
                        request.json.get('dateIn')])
                    conn.commit()
                    cursor.close()
                    conn.close()
                
                    return Response(status=201)
                except Exception as e:
                    print(e)
            else:
                return Response(status=401)
        
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
                    cursor.close()
                    conn.close()
                else:
                    pass
                return Response(status=200)

            except Exception as e:
                print(e)
        else:
            return Response(status=401)
