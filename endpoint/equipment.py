from app import app
from utilities import dbconn
from flask import request, Response
import json

@app.route("/api/equipment", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def equipment():
    conn = None
    cursor = None
    (conn, cursor) = dbconn()
    token = request.headers.get('token')
    
    if request.method == 'GET':
        params = request.args
        cursor.execute('SELECT user_id, role FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE login_token = ?', [token,])
        result = cursor.fetchone()
        if result[1] == ('admin'):
            cursor.execute('SELECT serial_number, product_description, in_stock from equipment')
            equip = cursor.fetchall()
            equipArray = []
            for equipment in equip:
                equipDict = {
                    'serial_number' : equipment[0],
                    'product_description' : equipment[1],
                    'in_stock' : equipment[2]
                }
                equipArray.append(equipDict)
            return Response(json.dumps(equipDict))
        else:
            return Response(json.dumps("You are unauthorized to make that request"),
                            mimetype='application/json',
                            status=403)
    elif request.method == 'POST':
        token = request.headers.get('token')
        cursor.execute('SELECT user_id, role FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE login_token = ?', [token,])
        result = cursor.fetchone()
        if result[1] == ('admin'):
            newProduct = cursor.execute('SELECT serial_number, product_description, in_stock from equipment WHERE serial_number = ?', [request.json.get('sn')] )
            cursor.execute("INSERT INTO equipment (serial_number, product_description, in_stock) VALUES (?, ?, ?)",[
                request.json.get('sn'),
                request.json.get('prod'),
                request.json.get('status'),])
            conn.commit(),
            
            cursor.close()
            conn.close()
            return Response(json.dumps(newProduct),
                            mimetype='application/json',
                            status=200)
        else:
            return Response(json.dumps("This product already exists"),
                            mimetype='application/json',
                            status=403)
            
    elif request.method == 'PATCH':
        cursor.execute('SELECT user_id, role FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE login_token = ?', [token,])
        result = cursor.fetchone()
        if result[1] == ('admin'):
            sn = request.json.get('sn')
            if request.json.get('prod') != None:
                cursor.execute('UPDATE equipment SET product_description = ? WHERE serial_number = ?', [request.json.get('prod'), sn])
            else:
                pass
            if request.json.get('status') == 'True':
                cursor.execute('UPDATE equipment SET in_stock = ? WHERE serial_number = ?',[0, sn,])
            else:
                pass
            if request.json.get('status') == 'False':
                    cursor.execute('UPDATE equipment SET in_stock = ? WHERE serial_number = ?',[1, sn,])
            else:
                pass
            cursor.execute('SELECT * FROM equipment WHERE serial_number = ?', [sn,])
            updated = cursor.fetchall()
            updateArray = []
            for update in updated:
                updateDict = {
                    'serial_number' : update[0],
                    'product_description' : update[1],
                    'in_stock' : update[2]
                }
                updateArray.append(updateDict)
            conn.commit()
            cursor.close()
            conn.close()
            return Response(json.dumps(updateDict, default=str),
                            mimetype='application.json',
                            status=200)        
        else:
            return Response(json.dumps("Failed to update"),
                            mimetype='application.json',
                            status=400)
    
    elif request.method == 'DELETE':
        cursor.execute('SELECT user_id, role FROM user_session INNER JOIN user ON user_session.user_id = user.id WHERE login_token = ?', [token,])
        result = cursor.fetchone()
        if result[1] == ('admin'):
            sn = request.json.get('sn')
            cursor.execute('SELECT * from equipment WHERE serial_number = ?'[sn,])
            result = cursor.fetchall()
            
            pass
            
            