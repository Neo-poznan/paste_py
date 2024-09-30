import logging
from datetime import datetime

import httpx

logger = logging.getLogger('django.request')

async def get_hash() -> str:
    '''Делает запрос к микросервису для получения ключа'''
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get('http://127.0.0.1:8001/generate/')
            if response.status_code != 200:
                raise httpx.HTTPError
            response_json = response.json()
            post_key = response_json['hash']  
            return post_key
    except httpx.HTTPError as e:
        logger.error(f'[{datetime.now()}] Ошибка при запросе к микросервису для генерации ключа! {e}')

        