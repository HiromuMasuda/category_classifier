from django.core.management.base import BaseCommand
from classification_machine.models import *
from classification_machine.modules.gunosy_article_scraper import *
from django.utils import timezone
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time


class Command(BaseCommand):
    help = 'Scraping article contents from Gunosy.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for category_page_url in self.get_category_page_urls():
            print("Scraping starts in ", category_page_url)

            category = int(category_page_url[-1])
            total_pages = 5
            article_urls = []

            for page_num in range(1, total_pages+1):
                url = category_page_url + "?page=" + str(page_num)
                scraper = GunosyArticleScraper(url)
                article_urls += scraper.get_article_urls()
                time.sleep(1)

            for article_url in article_urls:
                scraper = GunosyArticleScraper(article_url)

                try:
                    Article.objects.create(
                            title=scraper.get_article_title(),
                            content=scraper.get_article_content(),
                            category=category,
                            url=article_url,
                            updated_at=scraper.get_article_updated_at())
                except:
                    pass

                time.sleep(1)

    def get_category_page_urls(self):
        return [
            'https://gunosy.com/categories/1',  # エンタメ
            'https://gunosy.com/categories/2',  # スポーツ
            'https://gunosy.com/categories/3',  # おもしろ
            'https://gunosy.com/categories/4',  # 国内
            'https://gunosy.com/categories/5',  # 海外
            'https://gunosy.com/categories/6',  # コラム
            'https://gunosy.com/categories/7',  # IT・科学
            'https://gunosy.com/categories/8',  # グルメ
        ]
