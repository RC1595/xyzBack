from app import app
import sys
host='0.0.0.0'
port=5000

if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("Invalid mode, please choose either 'production' or 'testing'")
    exit()

if(mode == "production"):
    import bjoern
    print("Running in production mode!")
    bjoern.run(app, "0.0.0.0", 5001)
elif(mode == "testing"):
    from flask_cors import CORS
    CORS(app)
    print("Running in testing mode!")
    app.run(debug=True)
else:
    print("Invalid mode, please choose either 'production' or 'testing'")
    exit()