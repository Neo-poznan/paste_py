from typing import Never
from datetime import datetime
from datetime import timedelta

from django.core.exceptions import ValidationError

async def date_validator(date_str: str) -> Never:
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    today = date.today()
    max_date = today + timedelta(days=14)
    if date <= today:
        raise ValidationError('Дата удаления поста не может быть меньше сегодняшней даты')
    if date > max_date:
        raise ValidationError('Дата удаления поста не может быть больше 14 дней')
    
    