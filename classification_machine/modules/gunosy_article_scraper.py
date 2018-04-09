from django.core.management.base import BaseCommand
from classification_machine.models import *
from django.utils import timezone
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time

class GunosyArticleScraper:

    def __init__(self, article_url):
        self.article_url = article_url
        html = requests.get(article_url).text
        self.soup = BeautifulSoup(html, "html.parser")

    def get_title(self):
        return self.soup.find('h1', class_='article_header_title').text

    def get_content(self):
        contents = self.soup.find('div', class_='article gtm-click').find_all('p')
        content = ''
        for c in contents:
            content += c.text
        return content

    def get_updated_at(self):
        updated_at = self.soup.find('li', class_='article_header_lead_date')['content']
        updated_at = "{} {}".format(updated_at[:10], updated_at[11:19])
        updated_at = timezone.datetime.strptime(updated_at, '%Y-%m-%d %H:%M:%S')
        updated_at = timezone.make_aware(updated_at, timezone.get_current_timezone())
        return updated_at
