"""scraping
Scraping functions from gunosy
"""

from django.core.management.base import BaseCommand
from classification_machine.models import *
from django.utils import timezone
from bs4 import BeautifulSoup
from datetime import datetime
import requests


class UrlInvalidError(Exception):
    def __init__(self, message):
        self.message = message


class GunosyArticleScraper:

    def __init__(self, url):
        html = requests.get(url).text
        self.soup = BeautifulSoup(html, "html.parser")

    def get_article_urls(self):
        """scraping article urls from gunosy cateogry page

        Args:
            None

        Returns:
            list: article urls
        """
        article_urls = []
        try:
            list_titles = self.soup.find_all('div', class_="list_title")
        except:
            raise UrlInvalidError("Url may not be gunosy category page one.")

        for list_title in list_titles:
            article_url = list_title.find('a')['href']
            article_urls.append(article_url)
        return article_urls

    def get_article_title(self):
        """scraping article title from gunosy article page

        Args:
            None

        Returns:
            str: article title
        """
        try:
            title = self.soup.find('h1', class_='article_header_title').text
        except:
            raise UrlInvalidError("Url may not be gunosy article page one.")

        return title

    def get_article_content(self):
        """scraping article content from gunosy article page

        Args:
            None

        Returns:
            str: article content
        """
        try:
            contents = self.soup.find(
                    'div', class_='article gtm-click').find_all('p')
        except:
            raise UrlInvalidError("Url may not be gunosy article page one.")

        content = ''
        for c in contents:
            content += c.text
        return content

    def get_article_updated_at(self):
        """scraping article updated_at from gunosy article page

        Args:
            None

        Returns:
            datetime: article updated_at
        """
        try:
            updated_at = self.soup.find(
                    'li', class_='article_header_lead_date')['content']
        except:
            raise UrlInvalidError("Url may not be gunosy article page one.")

        updated_at = "{} {}".format(updated_at[:10], updated_at[11:19])
        updated_at = timezone.datetime.strptime(
                updated_at, '%Y-%m-%d %H:%M:%S')
        updated_at = timezone.make_aware(
                updated_at, timezone.get_current_timezone())
        return updated_at
