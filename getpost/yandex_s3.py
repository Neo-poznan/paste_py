import boto3
import logging
from datetime import datetime

from pastebin.settings import AWS_ACCESS_KEY_ID,  AWS_SECRET_ACCESS_KEY, ENDPOINT_URL

logger = logging.getLogger('django.request')

s3 = boto3.client(
    service_name='s3',
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    endpoint_url = ENDPOINT_URL,
)

def download_file_from_s3(url: str) -> str:
    '''
    достаем последнюю часть ссылки с ключом и бакетом
    получаем список из ключа и бакета и распаковываем его
    получаем объект из стореджа
    '''     
    bucket_key = url.split('/')[-1]   
    bucket, key = bucket_key.split('?key=')

    # получаем ответ от стореджа, достаем тело запроса и переделываем в читаемый текст
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
    except Exception as e:
        logger.error(f'[{datetime.now()}] Ошибка загрузки контента из S3! {e}')
        content = 'Ошибка загрузки контента!'
    return content

def delete_file_from_s3(url: str):
    '''
    достаем последнюю часть ссылки с ключом и бакетом
    получаем список из ключа и бакета и распаковываем его
    удаляем объект из стореджа
    '''         
    bucket_key = url.split('/')[-1]    
    bucket, key = bucket_key.split('?key=')
    try:
        s3.delete_object(Bucket=bucket,Key=key)
    except Exception as e:
        logger.error(f'[{datetime.now()}] Ошибка доступа к хранилищу при удалении контента из S3! {e}')

    