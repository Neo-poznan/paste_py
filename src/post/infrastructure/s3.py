import aioboto3
import logging
import botocore

from config.settings import AWS_ACCESS_KEY_ID,  AWS_SECRET_ACCESS_KEY, ENDPOINT_URL, CLIENT_FILES_BUCKET

logger = logging.getLogger('django.request')


async def upload_file_to_s3(content:str, key: str) -> None:
    session = aioboto3.Session()
    async with session.client(
        's3', endpoint_url=ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    ) as s3:
        try:
            await s3.put_object(Bucket=CLIENT_FILES_BUCKET, Key=key, Body=content)
        except botocore.exceptions.ClientError as e:
            logger.error(f'Error while uploading file to S3: {e}')
            raise PermissionError('Error accessing storage')


async def download_file_from_s3(key: str) -> str:
    key += '.txt'
    session = aioboto3.Session()
    async with session.client(
        's3', endpoint_url=ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        ) as client:
        try:
            response = await client.get_object(Bucket=CLIENT_FILES_BUCKET, Key=key)      
            post_content_bytes = await response['Body'].read()
            post_content = post_content_bytes.decode('utf-8')
            return post_content
        except client.exceptions.NoSuchKey as e:
            logger.error(f'Error while downloading file from S3: {e}')
            raise ValueError('File not found in storage')
        except botocore.exceptions.ClientError as e:
            logger.error(f'Error while downloading file from S3: {e}')
            raise PermissionError('Error accessing storage')


async def delete_file_from_s3(key: str) -> None:
    session = aioboto3.Session()
    async with session.client(
        's3', endpoint_url=ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        ) as s3:
        try:
            key += '.txt'
            await s3.delete_object(Bucket=CLIENT_FILES_BUCKET, Key=key)
        except botocore.exceptions.ClientError as e:
            logger.error(f'Error while deleting file from S3: {e}')
            raise PermissionError('Error accessing storage')

