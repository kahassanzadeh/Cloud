import os
import sys
import pika
from api.S3 import *
from api.image_procssing import *
import logging
from serv_1.src.database.postgres import *
from api.mail_service import send_email

def callback(ch, method, properties, body):
    state = ''
    body = body.decode()
    print(f'id:{body} Received')
    name_image1 = body + '_1.jpg'
    name_image2 = body + '_2.jpg'

    image1 = get_url(name_image1)
    image2 = get_url(name_image2)

    result_face_recognition, face_id_1, face_id_2 = face_recognition(image1, image2)

    if result_face_recognition:
        result_face_authentication = image_authentication(face_id_1, face_id_2)
        if result_face_authentication:
            eng.execute(f"UPDATE user_table SET state = 'accepted' WHERE id = {int(body)}; ")
        else:
            eng.execute(f"UPDATE user_table SET state = 'rejected' WHERE id = {int(body)}; ")

    else:
        eng.execute(f"UPDATE user_table SET state = 'rejected' WHERE id = {int(body)}; ")

    user = eng.execute(f"SELECT id,email,state FROM user_table WHERE id = {int(body)}").fetchone()
    send_email(user[1],user[2])


def main():
    url = os.environ.get('CLOUDAMQP_URL',
                         'amqps://bybyieoh:eKMpr-QzDlpRPLEAvttwHs3vHxOdn7uh@fish.rmq.cloudamqp.com/bybyieoh')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='users')

    channel.basic_consume(queue='users', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
