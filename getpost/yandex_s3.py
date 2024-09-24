import aioboto3
import os
import logging
from datetime import datetime

from pastebin.settings import AWS_ACCESS_KEY_ID,  AWS_SECRET_ACCESS_KEY, ENDPOINT_URL

logger = logging.getLogger('django.request')


async def download_file_from_s3(url: str) -> str:
    '''
    достаем последнюю часть ссылки с ключом и бакетом
    получаем список из ключа и бакета и распаковываем его
    создаем контекстный менеджер и данными хранилища
    получаем объект из стореджа в виде байтов и декодируем
    '''     
    bucket_key = url.split('/')[-1]
    print(bucket_key)
    bucket, key = bucket_key.split('?key=')
    try:
        session = aioboto3.Session()
        async with session.client(
                's3', endpoint_url=ENDPOINT_URL,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                ) as s3:
            response = await s3.get_object(Bucket=bucket, Key=key)      
            post_content_bytes = await response['Body'].read()
            post_content = post_content_bytes.decode('utf-8')
    except Exception as e:
        logger.error(f'[{datetime.now()}] Ошибка загрузки контента из S3! {e}')
        post_content = 'Ошибка загрузки контента!'
    return post_content

async def delete_file_from_s3(url: str) -> None:
    '''
    достаем последнюю часть ссылки с ключом и бакетом
    получаем список из ключа и бакета и распаковываем его
    создаем контекстный менеджер и данными хранилища
    удаляем объект из стореджа
    '''         
    bucket_key = url.split('/')[-1]    
    bucket, key = bucket_key.split('?key=')
    try:
        session = aioboto3.Session()
        async with session.client(
            's3', endpoint_url=ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            ) as s3:
            await s3.delete_object(Bucket=bucket,Key=key)
    except Exception as e:
        logger.error(f'[{datetime.now()}] Ошибка доступа к хранилищу при удалении контента из S3! {e}')

        