from flask import Flask, Response, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import cv2
import json
import os
import base64
import numpy as np
import boto3
import pymongo


def getConfig():
    try:
        with open("../config.json") as f:
            data = json.load(f)
        return data
    except:
        with open("config.json") as f:
            data = json.load(f)
        return data

# Initialize Flask app and SocketIO
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize boto3 client for Rekognition
rekognition = boto3.client('rekognition', region_name='us-east-1',
                           aws_access_key_id=getConfig().get("aws").get("access_key_id"),
                           aws_secret_access_key=getConfig().get("aws").get("secret_access_key"))

client = pymongo.MongoClient(getConfig().get("mongo"))
db = client.faceRecog
collection = db.databases

cascadePath = "cascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX

namesFILE = ""

try:
    namesFILE = "names.txt"
    with open(namesFILE) as f:
        pass
except:
    namesFILE = "api_v2/names.txt"
    with open(namesFILE) as f:
        pass

def getFaceIDMap():
    data = {}
    with open(namesFILE) as f:
        for line in f.readlines():
            line = line.strip().replace("\n","")
            if len(line)==0:
                continue
            data[line.split(":")[0]] = line.split(":")[-1]
    return data

def isFugitive(name: str):
    found = False
    if collection.find_one({"name": name}):
        if collection.find_one({"name": name}).get("suspect")==True:
            # add custom functions for robot dog
            return True
        else:
            # add custom functions for robot dog
            return False
    else:
        # add custom functions for robot dog
        return "UNKNOWN"

def detect_faces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.2, 6)
    
    recognized_faces = []

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        _, img_encoded = cv2.imencode('.jpg', roi_gray)
        img_bytes = img_encoded.tobytes()
        
        face_data = {
            'id': "Unknown",
            'fugitive': False,
            'pos_x': (round(float(x),2)),
            'pos_y': round(float(y),2),
            'pos_w': round(float(w),2),
            'pos_h': round(float(h),2)
        }

        try:            
            # Search for faces in the image using Rekognition
            response = rekognition.search_faces_by_image(
                CollectionId='face_db',
                Image={'Bytes': img_bytes}
            )
            
            # Process the recognized faces
            if response['FaceMatches']:
                face_data['id'] = response['FaceMatches'][0]['Face']['FaceId']
                face_data['id'] = getFaceIDMap().get(face_data['id'], "Unknown")
                
                fugitive_status = isFugitive(face_data['id'])
                if fugitive_status:
                    face_data['fugitive'] = True
                elif fugitive_status == 'UNKNOWN':
                    face_data['id'] = "Unknown"
                for key, value in collection.find_one({"name": face_data['id']}).items():
                    if key!="_id":
                        face_data[key] = value
        except Exception as e:
            print("Error during face recognition:", e)
        
        recognized_faces.append(face_data)
    
    return recognized_faces

@socketio.on('connect')
def handle_connect():
    pass

@socketio.on('disconnect')
def handle_disconnect():
    pass

@socketio.on('image')
def handle_image(image):
    try:
        _, img_data = image.split(',', 1)
        img_bytes = base64.b64decode(img_data)
        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        
        if len(img_array) > 0:
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            if img is not None:
                img = cv2.flip(img, 1)
                face_data = detect_faces(img)
                emit('response', face_data)
    except Exception as e:
        print("OOPS-AT-SOCKET",e)

@app.route('/video_capture')
def video_capture():
    return Response(capture_by_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/faceIDMap')
def return_face_id_map():
    return jsonify({"data":getFaceIDMap()})

@app.route('/add-user', methods=['POST'])
def add_user():
    uploaded_files = request.files.getlist("files")
    face_name = request.form.get("face_name")
    c = 0
    
    # List to store face IDs for indexing
    face_ids = []
    
    for file in uploaded_files:
        c += 1
        filename = file.filename
        
        img_stream = file.read()
        nparr = np.frombuffer(img_stream, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)

        if len(faces)!=0:
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.imwrite(os.path.join("datasets", f"User.{face_name}.{c}.{filename.split('.')[-1]}"), gray[y:y+h, x:x+w])
                
                # Index face using Rekognition
                response = rekognition.index_faces(
                    CollectionId='face_db',
                    Image={'Bytes': img_stream}
                )
                # Append the generated FaceID to the list
                if response.get('FaceRecords'):
                    if len(response['FaceRecords'])>=1:
                        face_ids.append(response['FaceRecords'][0]['Face']['FaceId'])
                        with open(filename, "a") as f:
                                f.write(f"{response['FaceRecords'][0]['Face']['FaceId']}:{face_name}\n")
                
    
    # Return the list of generated FaceIDs
    return jsonify({"message": "Files saved successfully.", "face_ids": face_ids})

if __name__=='__main__':
    socketio.run(app, debug=True, use_reloader=False, port=8888)