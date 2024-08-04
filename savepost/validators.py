from datetime import date, datetime
from django.core.exceptions import ValidationError

def date_validator(input_date):
    date_with_time =datetime.strptime(input_date)
    date = date_with_time.date()
    today = date.today()
    max_date = today + datetime.timedelta(days=14)
    if date <= today:
        raise ValidationError('Дата удаления поста не может быть меньше сегодняшней даты')
    if date > max_date:
        raise ValidationError('Дата удаления поста не может быть больше 14 дней')
    
    