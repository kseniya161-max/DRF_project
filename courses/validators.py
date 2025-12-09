from urllib.parse import urlparse

from rest_framework .serializers import ValidationError

allowed = ["youtube.com", "www.youtube.com"]

def link_validator(value):
    parsed_url = urlparse(value)
    if parsed_url.scheme not in ["http", "https"]:
        raise ValidationError("Вы не можете добавлять ссылки которые не начинаются с http и https")

    if parsed_url.netloc not in allowed:
        raise ValidationError("Вы не можете добавлять ссылки кроме youtube")
