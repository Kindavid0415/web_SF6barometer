from flask import Flask, jsonify, render_template, request
import requests
import numpy as np
import cv2
import json

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/result', methods=['POST'])
def result():
    try:
        input_image = request.files['file'].read()
        img_byte = np.frombuffer(input_image, np.uint8)
        img_decode = cv2.imdecode(img_byte, cv2.IMREAD_COLOR)
        cv2.imwrite(upload_path, img_decode)
        print('upload ok')
        files = {'image': input_image}
        data = {'filename': upload_file}
        res = requests.post(url=api_url, data=data, files=files)  # data支持字典或字符串
        if res.status_code == 200:
            result = json.loads(res.text)
            print(result)
        else:
            print("error")
        for det in result:
            cv2.rectangle(img_decode, (det[2], det[3]), (det[4], det[5]),\
                          colors[classes.index(det[1])], 10)
            cv2.rectangle(img_decode, (det[2], det[3]), (det[2] + 750, det[3] - 90),\
                          colors[classes.index(det[1])], thickness=-1)
            cv2.putText(img_decode, det[1]+' '+str(det[0]), (det[2], det[3] - 10),\
                        cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        cv2.imwrite(result_path, img_decode)
    except BaseException as e:
        print(e)
    return render_template('result.html')


if __name__ == '__main__':
    api_url = "http://192.168.0.65:8501"
    classes = ['abnormal', 'normal']
    colors = [(0, 0, 200), (0, 200, 0)]
    upload_file = 'upload.jpg'
    upload_path = r'static/images/upload.jpg'
    result_path = 'static/images/result.jpg'
    app.run(debug=True, host="0.0.0.0", port=4444, threaded=True)
