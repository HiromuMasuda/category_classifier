from django.core.management.base import BaseCommand
from classification_machine.models import *
from django.utils import timezone
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


class Command(BaseCommand):
    help = 'Scraping article contents from Gunosy.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        category_page_urls = [
            'https://gunosy.com/categories/1', # エンタメ
            'https://gunosy.com/categories/2', # スポーツ
            # 'https://gunosy.com/categories/3', # おもしろ
            # 'https://gunosy.com/categories/4', # 国内
            # 'https://gunosy.com/categories/5', # 海外
            # 'https://gunosy.com/categories/6', # コラム
            # 'https://gunosy.com/categories/7', # IT・科学
            # 'https://gunosy.com/categories/8', # グルメ
        ]

        for category_page_url in category_page_urls:
            category = int(category_page_url[-1])
            total_pages = 5
            article_urls = []

            for page_num in range(1, total_pages+1):
                url = category_page_url + "?page=" + str(page_num)
                html = requests.get(url).text
                soup = BeautifulSoup(html, "html.parser")

                list_titles = soup.find_all('div', class_="list_title")
                for list_title in list_titles:
                    article_url = list_title.find('a')['href']
                    article_urls.append(article_url)

                time.sleep(1)

            for article_url in article_urls:
                html = requests.get(article_url).text
                soup = BeautifulSoup(html, "html.parser")

                title = soup.find('h1', class_='article_header_title').text

                contents = soup.find('div', class_='article gtm-click').find_all('p')
                content = ''
                for c in contents:
                    content += c.text

                updated_at = soup.find('li', class_='article_header_lead_date')['content']
                updated_at = "{} {}".format(updated_at[:10], updated_at[11:19])
                updated_at = timezone.datetime.strptime(updated_at, '%Y-%m-%d %H:%M:%S')
                updated_at = timezone.make_aware(updated_at, timezone.get_current_timezone())

                Article.objects.create(title=title, content=content, category=category, updated_at=updated_at)

                time.sleep(1)
