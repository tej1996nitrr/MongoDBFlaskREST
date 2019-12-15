from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.secret_key = "secret"
# app.config['MONGO_URI'] ="mongodb://localhost:27017/Usersdb"
app.config['MONGO_URI'] = 'mongodb+srv://mongo:mongodb@mongocluster-lobek.mongodb.net/UserDB?retryWrites=true&w=majority'


mongo = PyMongo(app)


@app.route('/add',methods = ['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']
    if _name and _email and _password and request.method =='POST':
        _hashed_password =generate_password_hash(_password)
        # id = mongo.db.UsersCollection.insert_one({'name':_name,'email':_email,'pwd':_hashed_password})
        user_collection = mongo.db.Users
        user_collection.insert({'name':_name,'email':_email,'pwd':_hashed_password})

        resp = jsonify("User added successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/users')
def users():
    users = mongo.db.Users.find()
    resp = dumps(users)
    return resp

@app.errorhandler(404)
def not_found(error=None):
    message ={
        'status' :404,
        'message':'Not Found'+request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.route('/users/<id>')
def user(id):
    user  = mongo.db.Users.find_one({'_id':ObjectId(id)})
    resp  = dumps(user)
    return resp

@app.route('/delete/<id>',methods=['DELETE'])
def user_del(id):
    mongo.db.Users.delete_one({'_id':ObjectId(id)})
    resp = jsonify("User Deleted Successfully")
    resp.status_code = 200
    return resp

@app.route('/update/<id>',methods = ['PUT'])
def user_update(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _email and _password and _id and request.method =='PUT':
        _hashed_password = generate_password_hash(_password)
        mongo.db.Users.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name,'email':_email,'pwd':_hashed_password}})
        resp = jsonify("User Update Succesfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()
if __name__ =="__main__":
    app.run(debug=True)
