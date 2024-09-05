from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
import cv2
import yaml
import os, base64, json
import numpy as np
import requests
import boto3
import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)

def getURL():
    with open("../../config.json") as f:
        data = json.load(f)
    return data.get("urls").get("face_api")

def getConfig():
    with open("../../config.json") as f:
        data = json.load(f)
    return data


client = pymongo.MongoClient(getConfig().get("mongo"))
db = client.faceRecog
collection = db.databases

@app.route('/collect_data')
def collectData():
    cam = cv2.VideoCapture(0)
    face_detector = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
    face_id = request.args.get("name")
    if face_id==None:
        return {"message": "Face Name not input."}
    count = 0
    while(True):
        try:
            ret, img = cam.read()
            img = cv2.flip(img, 1) # 1 stright, 0 reverse
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                count += 1
                cv2.imwrite("datasets/User." + str(face_id.lower()) + '.' +  
                            str(count) + ".jpg", gray[y:y+h,x:x+w])
            k = cv2.waitKey(100) & 0xff
            if k == 27:
                break
            elif count >= 100:
                 break
        except:
            pass
    cam.release()
    cv2.destroyAllWindows()
    if request.args.get("sendToAPI"):
        files = [('files', open(f"datasets/User.{face_id.lower()}.{i}.jpg", 'rb')) for i in range(1, count+1)]
        face_name = request.args.get("name")
        api_url = f"http://{getURL().get('host')}:{getURL().get('port')}/add-user"
        payload = {"face_name": face_name}
        response = requests.post(api_url, files=files, data=payload)

        if response.status_code == 200:
            return {"message": "Added face successfully."}
        else:
            return {"message": "Error occurred while sending data to the API."}

    return render_template('done.html')

@app.route('/add-face')
def add_face():
    if collection.find_one({"name": request.args.get('name')}):
        return "<script>window.close()</script>"
    return render_template('add_face.html', name=request.args.get("name"))

@app.route('/delete-face')
def remove_face():
    id = request.args.get("id")
    if collection.find_one({ "_id" : ObjectId(str(id)) }):
        name = collection.find_one({ "_id" : ObjectId(str(id)) }).get("name").lower()
        # send req to api/faceIDMap to get key(id):valu(name)
        api_url = f"http://{getURL().get('host')}:{getURL().get('port')}/faceIDMap"
        idMap = requests.get(api_url).json().get("data")
        # delete all faces in rekog where key has name valu
        rekognition = boto3.client('rekognition', region_name='us-east-1',
                               aws_access_key_id=getConfig().get("aws").get("access_key_id"),
                               aws_secret_access_key=getConfig().get("aws").get("secret_access_key"))

        collection_id = 'face_db'
        region = 'us-east-1'

        for key, value in idMap.items():
            if name=='*':
                # List faces in the collection
                response = rekognition.list_faces(CollectionId=collection_id)

                # Delete all faces
                for face_record in response['Faces']:
                    face_id = face_record['FaceId']
                    rekognition.delete_faces(CollectionId=collection_id, FaceIds=[face_id])
                # print(f"All faces containing '{substring}' deleted successfully.")
                break
            if value==name:
                substring = key
                # try:
                # List faces in the collection
                response = rekognition.list_faces(CollectionId=collection_id)

                
                # Delete faces containing the substring in their external image ID
                for face_record in response['Faces']:
                    # print(face_record)
                    face_id = face_record['FaceId']
                    # print(face_id,substring)
                    if substring in face_id:
                        rekognition.delete_faces(CollectionId=collection_id, FaceIds=[face_id])
                # print(f"All faces containing '{substring}' deleted successfully.")
                # except Exception as e:
                #     # pass
                #     print(f"Error deleting faces: {e}")
    return "<script>window.close()</script>"

if __name__=='__main__':
    app.run(debug=True, use_reloader=False, port=7173)