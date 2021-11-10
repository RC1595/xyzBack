import mariadb
import dbcreds

conn = None
cursor = None

def dbconn():
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(
                                user = dbcreds.user,
                                password = dbcreds.password,
                                host = dbcreds.host,
                                port = dbcreds.port,
                                database = dbcreds.database)
        print("connected")
        cursor = conn.cursor()
    except:
        if (cursor != None):
            cursor.close()
        print("cursor closed")
        if (conn != None):
            conn.close()
        print("connection closed")
        raise ConnectionError ("Could not establish a connection to the database")
    return (conn, cursor)