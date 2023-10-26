import pika, sys, os, logging

url = os.environ.get('CLOUDAMQP_URL', 'amqps://bybyieoh:eKMpr-QzDlpRPLEAvttwHs3vHxOdn7uh@fish.rmq.cloudamqp.com/bybyieoh')
params = pika.URLParameters(url)


def send(msg):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='users')

    channel.basic_publish(exchange='', routing_key='users', body=msg)
    print(f"id = {msg} in RabbitMQ")
    connection.close()

if __name__ == '__main__':
    send("test")