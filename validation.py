import re


URL_PATTERN = re.compile(r"(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})(\.[a-zA-Z0-9]{2,})?")


def is_valid_url(url: str) -> bool:
    return bool(URL_PATTERN.match(url))