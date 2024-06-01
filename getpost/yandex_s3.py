import boto3

from pastebin.settings import AWS_ACCESE_KEY_ID,  AWS_SECRET_ACCESS_KEY, ENDPOINT_URL, CLIENT_FILES_BUCKET

s3 = boto3.client(
    service_name='s3',
    aws_access_key_id = AWS_ACCESE_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    endpoint_url = ENDPOINT_URL,
)
