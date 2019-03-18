"""Utils to check url"""
import re
from typing import Optional
from urllib.parse import urlparse

import scrapy


def check_is_url(url: str) -> bool:
    """Checks either the given string could be URL or not"""
    # Regular expression from WEB_URL_REGEX,
    # https://github.com/rcompton/ryancompton.net/blob/master/assets/praw_drugs/urlmarker.py
    url_regex = re.compile(
        r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:\w\w+)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:\w\w+)\b/?(?!@)))""")
    if url_regex.match(url):
        return True

    # Check if not only digits
    if url.isdigit():
        return False

    # Check if not only characters
    if url.isalpha():
        return False

    # Check if there is at least one dot
    if '.' not in url:
        return False
    elif url.startswith('.'):
        return False

    return True


def prettify_url(url: str):
    """Delete 'http[s]' and 'www' from a url"""
    url = url.replace('http://', '')
    url = url.replace('https://', '')
    if url.startswith('www.'):
        url = url.replace('www.', '')
    if url.endswith('/'):
        url = url[:-1]
    return url


def get_clean_url(url: str) -> Optional[str]:
    """Add 'http://' prefix for url if it not exist"""
    if not check_is_url(url):
        return None

    # delete whitespaces around the url
    url = url.strip()

    # requests package needs in protocol in URL
    if not url.startswith('http'):
        url = 'http://' + url
    # requests with '/' url's endings sometimes gets 404 error
    if url.endswith('/'):
        url = url[:-1]
    return scrapy.utils.url.canonicalize_url(url)


def extract_domain(url: str) -> str:
    """Extract domain from raw url"""
    url = urlparse(get_clean_url(url)).netloc
    return url

