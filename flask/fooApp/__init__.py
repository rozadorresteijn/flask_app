from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

# app.config['MONGO_DBNAME'] = 'foodb'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/foodb'



app.config['MONGO_DBNAME'] = <namedatabase>
app.config['MONGO_URI'] =
            "mongodb://<user>:<password>@<URLdatabase>.mlab.com:57066/<namedatabase>"

mongo = PyMongo(app)