from django.core.management.base import BaseCommand
from asgiref.sync import async_to_sync

class Command(BaseCommand):
    help = 'Delete outdated posts'

    def handle(self, *args, **options) -> None:
        '''
        Получаем все посты с сегодняшней датой удаления
        проходимся по queryset и сначала удаляем из с3 а потом из базы данных
        '''
        from post.models import Posts
        from django.utils import timezone
        from post.infrastructure.s3 import delete_file_from_s3
        outdated_posts = Posts.objects.filter(del_date=timezone.now())
        for post in outdated_posts:
            async_to_sync(delete_file_from_s3)(post.key)
            post.delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted outdated posts'))

