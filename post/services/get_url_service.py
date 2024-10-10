import logging
from datetime import datetime

import httpx

from pastebin.settings import HASH_GENERATOR_URL

logger = logging.getLogger('django.request')


async def get_hash() -> str:
    '''Делает запрос к микросервису для получения ключа'''
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(HASH_GENERATOR_URL)
            if response.status_code != 200:
                raise httpx.HTTPError
            response_json = response.json()
            post_key = response_json['hash']  
            return post_key
    except httpx.HTTPError as e:
        logger.error(f'[{datetime.now()}] Ошибка при запросе к микросервису для генерации ключа! {e}')

        