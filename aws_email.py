#!/usr/bin/env python3
import boto3, logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

sender = "luke.x.rickard@gmail.com"
recipient = "luke.rickard@gmail.com"
awsregion = "us-east-1"

# The subject line for the email.
subject = "Amazon SES Test (SDK for Python)"

# The HTML body of the email.
htmlbody = """<h1>Amazon SES Test (SDK for Python)</h1><p>This email was sent with 
            <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the 
            <a href='https://aws.amazon.com/sdk-for-python/'>AWS SDK for Python (Boto)</a>.</p>"""

# The email body for recipients with non-HTML email clients.  
textbody = "This email was sent with Amazon SES using the AWS SDK for Python (Boto)"

# The character encoding for the email.
charset = "UTF-8"

class AwsEmail():

	def __init__(self):
		# Create a new SES resource and specify a region.
		self.client = boto3.client('ses',region_name=awsregion)

	def send_email(self):
		try:
			logger.info("Sending email to %s", recipient)
			response = self.client.send_email(
		        Destination={
		            'ToAddresses': [
		                recipient,
		            ],
		        },
		        Message={
		            'Body': {
		                'Html': {
		                    'Charset': charset,
		                    'Data': htmlbody,
		                },
		                'Text': {
		                    'Charset': charset,
		                    'Data': textbody,
		                },
		            },
		            'Subject': {
		                'Charset': charset,
		                'Data': subject,
		            },
		        },
		        Source=sender,
		    )
		except ClientError as e:
			logger.error(e.response['Error']['Message'])
		else:
			logger.info("Email sent! Message ID:%s", response['ResponseMetadata']['RequestId'])




