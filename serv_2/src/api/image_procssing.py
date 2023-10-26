import requests
#from api.S3 import *

api_key = 'acc_f78606957d969d2'
api_secret = 'fd68670fb4c935ed57156847999fdc92'


def image_authentication(face_id_1, face_id_2):
    # response_1 = requests.get(
    #     'https://api.imagga.com/v2/faces/detections?return_face_id=1&&image_url=%s' % url1,
    #     auth=(api_key, api_secret))
    #
    # response_2 = requests.get(
    #     'https://api.imagga.com/v2/faces/detections?return_face_id=1&&image_url=%s' % url2,
    #     auth=(api_key, api_secret))
    # response_json_1 = response_1.json()
    # response_json_2 = response_2.json()
    # face_id_1 = response_json_1["result"]["faces"][0]["face_id"]
    # face_id_2 = response_json_2["result"]["faces"][0]["face_id"]

    response = requests.get(
        'https://api.imagga.com/v2/faces/similarity?face_id=%s&second_face_id=%s' % (face_id_1, face_id_2),
        auth=(api_key, api_secret))

    response_json = response.json()
    if response_json["result"]["score"] >= 70:
        return True
    else:
        return False


def face_recognition(url1, url2):
    response_1 = requests.get(
        'https://api.imagga.com/v2/faces/detections?return_face_id=1&&image_url=%s' % url1,
        auth=(api_key, api_secret))

    response_2 = requests.get(
        'https://api.imagga.com/v2/faces/detections?return_face_id=1&&image_url=%s' % url2,
        auth=(api_key, api_secret))
    response_json_1 = response_1.json()
    response_json_2 = response_2.json()
    if response_json_1["result"]["faces"][0]["confidence"] <= 80 or response_json_2["result"]["faces"][0]["confidence"] <= 80:
        return False, 0, 0
    else:
        return True, response_json_1["result"]["faces"][0]["face_id"], response_json_2["result"]["faces"][0]["face_id"]

if __name__ == "__main__":
    # response_1 = requests.get(
    #     'https://api.imagga.com/v2/faces/detections?image_url=%s' % get_url('1_1.jpg'),
    #     auth=(api_key, api_secret))
    # response_json_1 = response_1.json()
    # print(response_json_1)


    # image_path = '/Users/kamyar/Desktop/images.jpeg'
    #
    # response = requests.post(
    #     'https://api.imagga.com/v2/faces/detections?return_face_id=1',
    #     auth=(api_key, api_secret),
    #     files={'image': open(image_path, 'rb')})
    # d = response.json()
    # print(d)
    response_1 = requests.get(
        'https://api.imagga.com/v2/faces/detections?image_url=%s' % "https://c999289.parspack.net/c999289/1_1.jpg",
        auth=(api_key, api_secret))
    print(response_1)