from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import cv2
from datetime import datetime
import os
import string
import io
import random
from detect_squares import detect_postit

SAVE_ROOT = "./static/uploads"
if not os.path.isdir(SAVE_ROOT):
    os.mkdir(SAVE_ROOT)

app = Flask(__name__)

def random_str(n):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])

@app.route('/')
def index():
    # print(os.listdir(SAVE_ROOT)[::-1])
    import glob
    img_list = []
    folder_list = os.listdir(SAVE_ROOT)[::-1]
    for folder in folder_list:
        text = os.path.join(SAVE_ROOT, folder)
        imgs = glob.glob(text + "/*.jpg")
        img_list.append(imgs)

    return render_template('index.html', images=img_list)

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory(SAVE_ROOT, path)

# 参考: https://qiita.com/yuuuu3/items/6e4206fdc8c83747544b
@app.route('/upload', methods=['POST'])
def upload():
    if request.files['image']:
        # 画像として読み込み
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, 1)

        
        foldername = datetime.now().strftime("%Y_%m_%d%_H_%M_%S_")
        save_dir = os.path.join(SAVE_ROOT, foldername)
        os.makedirs(save_dir, exist_ok=True)

        # 変換
        detect_postit(img, save_dir)

        return redirect('/')

if __name__ == '__main__':
    app.debug = True
    app.run()