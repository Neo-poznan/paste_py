import boto3

from pastebin.settings import AWS_ACCESE_KEY_ID,  AWS_SECRET_ACCESS_KEY, ENDPOINT_URL

s3 = boto3.client(
    service_name='s3',
    aws_access_key_id = AWS_ACCESE_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    endpoint_url = ENDPOINT_URL,
)

def download_file_from_s3(url):
    bucket_key = url.split('/')[-1]
    bucket, key = bucket_key.split('?key=')

    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    return content
