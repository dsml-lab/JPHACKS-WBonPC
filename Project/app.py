from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import cv2
from datetime import datetime
import os
import string
import io
import random
from detect_squares import detect_squares

SAVE_DIR = "./static/uploads"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)

app = Flask(__name__)

def random_str(n):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])

@app.route('/')
def index():
    print(os.listdir(SAVE_DIR)[::-1])
    return render_template('index.html', images=os.listdir(SAVE_DIR)[::-1])

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory(SAVE_DIR, path)

# 参考: https://qiita.com/yuuuu3/items/6e4206fdc8c83747544b
@app.route('/upload', methods=['POST'])
def upload():
    if request.files['image']:
        # 画像として読み込み
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, 1)

        # 変換
        img = detect_squares(img)

        # 保存
        filename = datetime.now().strftime("%Y_%m_%d%_H_%M_%S_") + random_str(5) + ".jpg"
        save_path = os.path.join(SAVE_DIR, filename)
        cv2.imwrite(save_path, img)

        print("save", save_path)

        return redirect('/')

if __name__ == '__main__':
    app.debug = True
    app.run()