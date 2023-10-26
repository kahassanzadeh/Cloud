import logging
import boto3
import sys
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)

domain = 'https://c999289.parspack.net'
bucket_name = 'c999289'
access_key = 'CksrrJ7KKfNv5Rzc'
secret_key = 'klpvTT3wSKTpAsOtkc6qcNHH4Zyj6dfl'

try:
    s3 = boto3.resource(
        's3',
        endpoint_url=domain,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
except Exception as e:
    logging.info(e)
else:
    bucket = s3.Bucket(bucket_name)


def list_files():
    for object in bucket.objects.all():
        logging.info(f"object_name: {object.key}, last_modified: {object.last_modified}")


def upload_file(file, object_name):
    contents = file.file.read()
    bucket.put_object(
        ACL='private',
        Body=contents,
        Key=object_name
    )
    print(f'{object_name} successfully uploaded')


def get_url(filename):
    # filename = str(filename).split("'")[1]
    url = f"{domain}/{bucket_name}/{filename}"
    return url


def download_file(object_name, download_path):
    bucket.download_file(
        object_name,
        download_path
    )


def delete_file(object_name):
    object_name = 'parspack.png'
    object = bucket.Object(object_name)
    object.delete()
