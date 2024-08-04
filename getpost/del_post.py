from savepost.models import PostUrls
from datetime import date
from getpost.yandex_s3 import delete_file_from_s3

def del_post():
    while True:
        posts = PostUrls.objects.filter(del_date=date.today())
        for post in posts:
            print(post)
            delete_file_from_s3(post.file_url)
            post.delete()

