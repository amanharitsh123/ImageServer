import os
from flask import Flask, request, jsonify
from neo4jIO import DB
import uuid

currentDB = DB()
app = Flask(__name__)

@app.route('/checkFriend', methods=['POST'])
def checkFriend():
    try:
        friend1 = request.json['friend1']
        friend2 = request.json['friend2']
        res = {'status':str(currentDB.ifFriend(friend1, friend2))}
        return jsonify(res)
    except:
        return "incorrect API use", 500

@app.route('/makeFriend', methods=['POST'])
def makeFriend():
    try:
        friend1 = request.json['friend1']
        friend2 = request.json['friend2']
        rstr = currentDB.makeFriend(friend1, friend2)
        print("rstr is ", rstr)
        res = {'status':rstr}
        return jsonify(res)
    except:
        return "incorrect API use", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001,  debug=True)