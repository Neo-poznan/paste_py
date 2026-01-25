from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Cache most viewed posts'

    def handle(self, *args, **options):
        '''
        Достанем заданное количество постов с наибольшим количеством просмотров
        и которые просматривались заданное время назад и кэшируем текст поста
        '''
        import redis
        from django.db import connection
        
        from config.settings import REDIS_HOST, REDIS_PORT, MOST_VIEWED_POSTS_LIMIT
        from config.settings import MOST_VIEWED_POSTS_CACHE_TIME, TIME_TO_CHECK_POST_VIEWS
        from post.services.s3 import download_file_from_s3
        redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
        cursor = connection.cursor()
        cursor.execute(
            f'''
            select key 
            from savepost_posts
            where last_query > datetime('now','-{TIME_TO_CHECK_POST_VIEWS} hour')
            order by views_count desc
            limit {MOST_VIEWED_POSTS_LIMIT}
            '''
        )
        most_viewed_posts = cursor.fetchall()
        for post in most_viewed_posts:
            if not redis_client.exists(post[0]):
                post_content = download_file_from_s3(post[0] + '.txt')
                redis_client.set(post[0], post_content)
                redis_client.expire(post[0], MOST_VIEWED_POSTS_CACHE_TIME)              

