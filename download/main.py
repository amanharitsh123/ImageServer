import os
from flask import Flask, request, render_template, send_from_directory
import uuid
import jinja2
from redisIO import *

UPLOAD_FOLDER = '../upload/upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/download', methods=['POST'])
def downlaod():
    result = request.form.to_dict(flat=False)
    data = {'userid':result['userid'][0], 'image':result['image'][0]}
    userid = result['userid'][0]
    image = result['image'][0]
    path = os.path.join(app.config['UPLOAD_FOLDER'])
    print(path)
    return send_from_directory(path, image)

@app.route('/', methods=['GET', 'POST'])
def downlaod_file():
    image = request.args.get('image', default = 1, type = int)
    if image == 1:
        data = get_all_filenames()
        loader = jinja2.FileSystemLoader('templates/download.html')
        env = jinja2.Environment(loader=loader)
        template = env.get_template('')
        return template.render(items=data)
    else:
        # Check for connections and file download
        pass



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)