from typing import Never
from datetime import datetime
from datetime import timedelta

from django.core.exceptions import ValidationError


def post_date_validator(date_str: str) -> Never:
    '''
    Проверить чтобы дата была больше сегодняшей и меньше 60 дней после это нужно
    чтобы нельзя было, посылая запросы вручную, захламить хранилище постами, которые нельзя удалить
    '''
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    today = date.today()
    max_date = today + timedelta(days=60)
    if date <= today:
        raise ValidationError('Дата удаления поста не может быть меньше сегодняшней даты')
    if date > max_date:
        raise ValidationError('Дата удаления поста не может быть больше 60 дней')
    
    