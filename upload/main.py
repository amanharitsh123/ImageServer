import os
from flask import Flask, request
from redisIO import *
import uuid

UPLOAD_FOLDER = './upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        unique_filename = str(uuid.uuid4())
        path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file1.save(path)
        data = request.form.to_dict(flat=False)
        userId = data['userid'][0]
        # Set userid and filename
        set_UserID(userId, unique_filename)
        set_filename(userId, unique_filename)
        return path
    return '''
    <h1>Upload new File</h1>
    <form method="post" enctype="multipart/form-data">
    UserId: <input type="text" name="userid"> <br>
    File: <input type="file" name="file1">
    <input type="submit">
    </form>
    '''

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)