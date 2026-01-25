import aioboto3
import logging
from datetime import datetime

from config.settings import AWS_ACCESS_KEY_ID,  AWS_SECRET_ACCESS_KEY, ENDPOINT_URL, CLIENT_FILES_BUCKET

logger = logging.getLogger('django.request')


async def upload_file_to_s3(content:str, key: str) -> None:
    '''
    Записываем контент в облако
    '''
    session = aioboto3.Session()
    async with session.client(
        's3', endpoint_url=ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    ) as s3:
        await s3.put_object(Bucket=CLIENT_FILES_BUCKET, Key=key, Body=content)


async def download_file_from_s3(key: str) -> str:
    '''
    создаем контекстный менеджер c данными хранилища
    получаем объект из стореджа в виде байтов и декодируем
    '''     
    key += '.txt'
    try:
        session = aioboto3.Session()
        async with session.client(
                's3', endpoint_url=ENDPOINT_URL,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                ) as s3:
            response = await s3.get_object(Bucket=CLIENT_FILES_BUCKET, Key=key)      
            post_content_bytes = await response['Body'].read()
            post_content = post_content_bytes.decode('utf-8')
    except Exception as e:
        logger.error(f'[{datetime.now()}] Ошибка загрузки контента из S3! {e}')
        post_content = 'Ошибка загрузки контента!'
    return post_content


async def delete_file_from_s3(key: str) -> None:
    '''
    создаем контекстный менеджер c данными хранилища
    удаляем объект из стореджа
    '''         
    key += '.txt'
    try:
        session = aioboto3.Session()
        async with session.client(
            's3', endpoint_url=ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            ) as s3:
            await s3.delete_object(Bucket=CLIENT_FILES_BUCKET, Key=key)
    except Exception as e:
        logger.error(f'[{datetime.now()}] Ошибка доступа к хранилищу при удалении контента из S3! {e}')
        
