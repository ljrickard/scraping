#!/usr/bin/env python3
import boto3
import logging
import json
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
awsregion = "us-east-1"


class AwsEmail():

    def __init__(self):
        # Create a new SES resource and specify a region.
        self.client = boto3.client('ses', region_name=awsregion)

    def send_email(self, data):
        try:
            logger.info("Sending email to %s", data['recipient'])
            response = self.client.send_email(
                Destination={
                    'ToAddresses': [
                        data['recipient'],
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': data['charset'],
                            'Data': data['body'],
                        },
                    },
                    'Subject': {
                        'Charset': data['charset'],
                        'Data': data['subject'],
                    },
                },
                Source=data['sender'],
            )
        except ClientError as e:
            logger.error(e.response['Error']['Message'])
        else:
            logger.info("Email sent! Message ID:%s",
                        response['ResponseMetadata']['RequestId'])
