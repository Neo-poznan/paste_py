import boto3

from pastebin.settings import AWS_ACCESE_KEY_ID,  AWS_SECRET_ACCESS_KEY, ENDPOINT_URL, CLIENT_FILES_BUCKET

s3 = boto3.client(
    service_name='s3',
    aws_access_key_id = AWS_ACCESE_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    endpoint_url = ENDPOINT_URL,
)

def upload_file_to_s3(text, key):
    key += '.txt'
    file = ''
    # уберем из текста все лишние переносы строки, т.к. textarea зачем-то ставит их в начало и конец каждой строки
    for line in text.split('\n'): 
        file += line.strip() + '\n'    
    try:
        # загрузим файл в облако
        s3.put_object(Bucket=CLIENT_FILES_BUCKET, Key=key, Body=file)
        # сделаем ссылку на него, тут должна быть ссылка именно на твое облако
        file_url = f"https://console.yandex.cloud/folders/b1ghi85fci38pckmj0ns/storage/buckets/{CLIENT_FILES_BUCKET}?key={key}"
    except Exception as exce:
        print(exce)
    return file_url



    
    

    