import aioboto3
import logging
from datetime import datetime

from pastebin.settings import AWS_ACCESS_KEY_ID,  AWS_SECRET_ACCESS_KEY, ENDPOINT_URL, CLIENT_FILES_BUCKET

logger = logging.getLogger('django.request')

async def upload_file_to_s3(content:str, key: str) -> None:
    '''
    Удалим лишние пробелы, табуляции и переносы строк и заменим их
    на один перенос строки. Запишем в облако и вернем ссылку
    '''
    key += '.txt'
    content_without_unnecessary_line_breaks = ''
    content = content.strip()
    for line in content.split('\n'): 
        content_without_unnecessary_line_breaks += line.strip() + '\n'   
    try:
        session = aioboto3.Session()
        async with session.client(
            's3', endpoint_url=ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        ) as s3:
            await s3.put_object(Bucket=CLIENT_FILES_BUCKET, Key=key, Body=content_without_unnecessary_line_breaks)
    except Exception as e:
        logger.error(f'[{datetime.now()}] Ошибка запроса к хранилищу при записи файла в облако: {e}')
        
