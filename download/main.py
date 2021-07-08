from connection.main import checkFriend
import os
from flask import Flask, request, render_template, send_from_directory
import uuid
import jinja2
from redisIO import *
import requests

UPLOAD_FOLDER = '../upload/upload'

app = Flask(__name__)
url_checkfriend = "http://localhost:5003/checkFriend"
url_makeFriend = "http://localhost:5003/makeFriend"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def checkFriend(user1, user2):
    data = {'friend1':user1, 'friend2':user2}
    res = requests.post(url_checkfriend, data=data)
    try:
        ans = res.json()['status']
        return True
    except:
        return False

def makeFriend(user1, user2):
    data = {'friend1':user1, 'friend2':user2}
    try:
        res = requests.post(url_checkfriend, data=data)
        print("friend added successfully")
    except:
        print("adding friend failed")


@app.route('/', methods=['GET', 'POST'])
def downlaod_file():
    if request.method=='GET':
        data = get_all_filenames()
        loader = jinja2.FileSystemLoader('templates/download.html')
        env = jinja2.Environment(loader=loader)
        template = env.get_template('')
        return template.render(items=data)
    else:
        # Check for connections and file download
        result = request.form.to_dict(flat=False)
        data = {'userid':result['userid'][0], 'image':result['image'][0]}
        user1 = result['userid'][0]
        image = result['image'][0]
        user2 = get_by_filename(image)
        if checkFriend(user1, user2):
            path = os.path.join(app.config['UPLOAD_FOLDER'])
            print(path)
            return send_from_directory(path, image)
        else:
            makeFriend(user1, user2)
            return "Access denied, file belongs to a differnet user. Added as friends, try again!"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)