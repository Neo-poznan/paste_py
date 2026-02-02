import aioboto3
import redis

from typing import NoReturn, Union

from django.db import connection

from config.settings import REDIS_HOST, REDIS_PORT, SERVER_URL

from post.infrastructure.url_generator import get_key
from post.infrastructure.s3 import download_file_from_s3, upload_file_to_s3
from post.validators import post_date_validator
from post.models import Posts

async def create_post(s3_session: aioboto3.Session, post_content: str, expire_date: str) -> str:
    post_key = await get_key(connection=connection, redis_host=REDIS_HOST, redis_port=REDIS_PORT)
    post_date_validator(expire_date)
    post_content = await remove_unnecessary_line_breaks(post_content)
    post_filename = post_key + '.txt'
    await upload_file_to_s3(s3_session, post_content, post_filename)
    await Posts.objects.acreate(key=post_key, delete_date=expire_date)
    # Formatting the URL to send back to the user
    url = f'{SERVER_URL}/p/{post_key}'
    return url

async def get_post(s3_session: aioboto3.Session, post_key: str, need_update_views_count: bool) -> Union[str, NoReturn]:
    post_metadata = await Posts.objects.aget(key=post_key)
    if need_update_views_count:
        post_metadata.views_count += 1
    # update the last access date and views count
    await post_metadata.asave()
    # get the post text
    post_content = await get_post_content(s3_session, post_key)
    return {'post_content': post_content, 'views': post_metadata.views_count}

async def remove_unnecessary_line_breaks(content: str) -> str:
    '''
    Remove unnecessary line breaks from the post content.
    '''
    content_without_unnecessary_line_breaks = ''
    content = content.strip()
    for line in content.split('\n'):
        content_without_unnecessary_line_breaks += line.strip('\n') + '\n'   
    return content_without_unnecessary_line_breaks

async def get_post_content(s3_session: aioboto3.Session, post_key: str) -> Union[str, None]:
    '''
    If the post content is cached in Redis, get it from there.
    Otherwise, download it from S3, cache it in Redis for 30 minutes, and return it.
    '''
    
    async with redis.asyncio.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}/0') as redis_client:
        if await redis_client.exists(post_key):
            return (await redis_client.get(post_key)).decode('utf-8')
        post_content = await download_file_from_s3(s3_session, post_key)
        if post_content:
            await redis_client.set(post_key, post_content)
            await redis_client.expire(post_key, 1800) 
        return post_content

    