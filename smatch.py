import http.client, urllib.request, urllib.parse, urllib.error, base64
import sys
import json
import os

API_BASE = 'eastus.api.cognitive.microsoft.com'
API_VERSION = '/face/v1.0'
API_DETECT_ENDPOINT = '/detect'
API_VERIFY_ENDPOINT = '/verify'
SUBSCRIPTION_KEY = os.environ['MSKEY']
ID_KEY = 'faceId'

def call_api(endpoint, params, data, headers):
    conn = http.client.HTTPSConnection(API_BASE)
    url = "{}{}?{}".format(API_VERSION, endpoint, params)
    print('URL: {}'.format(url))
    conn.request("POST", url, data, headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    print('Response: {}'.format(data))
    conn.close()
    json_obj = json.loads(data)
    return json_obj

def detect_face(img_path):
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        # 'returnFaceAttributes': '{string}',
    })
    json_obj = call_api(API_DETECT_ENDPOINT, params, open(img_path, 'rb'), headers)
    print(json_obj)
    return json_obj

def verify_face(faceId1, faceId2):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
    }

    params = urllib.parse.urlencode({})
    json_obj = call_api(
        API_VERIFY_ENDPOINT, 
        params, 
        str({
            "faceId1": faceId1,
            "faceId2": faceId2
        }), 
        headers
    )
    print(json_obj)
    return json_obj

def getId(face):
    return face[0][ID_KEY]


img1 = sys.argv[1]
img2 = sys.argv[2]

face1 = detect_face(img1)
print(face1)

face2 = detect_face(img2)
print(face2)

try:
    verified = verify_face(getId(face1), getId(face2))
except Exception as e:
    print(e)