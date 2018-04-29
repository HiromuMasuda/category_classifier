"""scrape_articles
Custom command for scraping articles from gunosy
and storing them to database
command: python manage.py scrape_articles
"""

from django.core.management.base import BaseCommand
from classification_machine.models import Article
from classification_machine.modules.gunosy_article_scraper import (
        GunosyArticleScraper
        )
from classification_machine.static import consts
from django.utils import timezone
from urllib.parse import urlencode
import time


class Command(BaseCommand):
    help = 'Scraping article contents from Gunosy.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        category_page_urls = \
                [val['url'] for val in consts.GUNOSY_CATEGORIES_DICT.values()]
        TOTAL_PAGES = 5

        for category_page_url in category_page_urls:
            print("Scraping starts in ", category_page_url)

            category = int(category_page_url[-1])
            article_urls = []

            for page_num in range(1, TOTAL_PAGES+1):
                url = "{}?{}".format(
                        category_page_url, urlencode({'page': str(page_num)}))
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
                except Exception as e:
                    print(type(e).__name__, e)

                time.sleep(1)
