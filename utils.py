#!/usr/bin/env python3
import requests
import boto3
import uuid

LOCAL_CACHE = 'cache/'
BUCKET_NAME = '5b05dbe9-c0b8-493e-8b05-7b5422887779'
AWS_BASE_URL = 'https://s3.amazonaws.com'

#https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
def _download_file(url):
	file_name = str(uuid.uuid4()) + '.jpg'
	file_location = LOCAL_CACHE + file_name
	r = requests.get(url, stream=True)
	with open(file_location, 'wb') as f:
	    for chunk in r.iter_content(chunk_size=1024): 
	        if chunk: # filter out keep-alive new chunks
	            f.write(chunk)
	return file_name

class aws():

	def __init__(self):
		self.s3_client = boto3.client('s3')
		self.s3_resource = boto3.resource('s3')

	def save_to_s3(self, url):
		file_name = _download_file(url)
		self.s3_client.upload_file(LOCAL_CACHE+file_name, BUCKET_NAME, file_name, ExtraArgs={'ContentType':'image/jpg'})
		self.s3_resource.Bucket(BUCKET_NAME).Object(file_name).Acl().put(ACL='public-read')
		return AWS_BASE_URL+'/'+BUCKET_NAME+'/'+file_name

