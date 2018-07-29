#!/usr/bin/env python3
import requests
import logging
import boto3
import uuid
import os
import random

LOCAL_CACHE = 'cache/'
BUCKET_NAME = '287554b7-2564-4d05-aab5-952b606fe3a1'
AWS_BASE_URL = 'https://s3.amazonaws.com'

logger = logging.getLogger(__name__)

# https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py

def _download_file(url, product_id):
    random_string = ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(16))
    file_name = product_id + '-' + random_string + '.jpg' #str(uuid.uuid4()) + '.jpg'
    file_location = LOCAL_CACHE + file_name
    r = requests.get(url, stream=True)
    with open(file_location, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return file_name


class AwsS3():

    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')

    def save_image_to_s3(self, url, product_id):
        file_name = _download_file(url, product_id)
        logger.info('Saving image URL=%s with filename=%s to s3 to bucket %s', url, file_name, BUCKET_NAME)
        self.s3_client.upload_file(LOCAL_CACHE + file_name, BUCKET_NAME, file_name, ExtraArgs={'ContentType': 'image/jpg'})
        self.s3_resource.Bucket(BUCKET_NAME).Object(file_name).Acl().put(ACL='public-read')
        self._remove_local_copy(LOCAL_CACHE + file_name)
        return AWS_BASE_URL + '/' + BUCKET_NAME + '/' + file_name

    def _remove_local_copy(self, file):
        os.remove(file)

    def clear_all_images(self):
        logger.info('Removing all items from %s bucket', BUCKET_NAME)
        full_bucket = self.s3_resource.Bucket(BUCKET_NAME)
        for key in full_bucket.objects.all():
            key.delete()
