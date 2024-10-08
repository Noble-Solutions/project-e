import urllib.parse


def generate_signed_url(url_fields_dictionary: dict) -> str:
    # Извлекаем информацию из входного объекта
    bucket_url = url_fields_dictionary["url"]
    fields = url_fields_dictionary["fields"]

    # Извлекаем имя бакета из URL
    bucket_name = bucket_url.split("/")[2].split(".")[0]

    # Формируем базовый URL для объекта
    object_name = fields["key"]
    base_url = f"https://{bucket_name}.storage.yandexcloud.net/{object_name}"

    # Формируем параметры запроса
    query_params = {
        "X-Amz-Algorithm": fields["x-amz-algorithm"],
        "X-Amz-Credential": fields["x-amz-credential"],
        "X-Amz-Date": fields["x-amz-date"],
        "X-Amz-Expires": "3600",  # Установим время истечения в 1 час
        "X-Amz-SignedHeaders": "host",
        "X-Amz-Signature": fields["x-amz-signature"],
    }

    # Кодируем параметры запроса
    encoded_params = urllib.parse.urlencode(query_params)

    # Формируем полный URL
    signed_url = f"{base_url}?{encoded_params}"

    return signed_url


# Пример использования
data = {
    "url": "https://storage.yandexcloud.net/project-e-bucket",
    "fields": {
        "key": "task1.txt",
        "x-amz-algorithm": "AWS4-HMAC-SHA256",
        "x-amz-credential": "string/20241004/ru-central1/s3/aws4_request",
        "x-amz-date": "20241004T082040Z",
        "policy": "string",
        "x-amz-signature": "76b4d6b2444140c57898e36b5906c338043184232f7f7ca3384fcda1537c9205",
    },
}
