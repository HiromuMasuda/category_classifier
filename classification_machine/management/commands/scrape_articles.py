from django.core.management.base import BaseCommand
from classification_machine.models import *


class Command(BaseCommand):
    help = 'Scraping article contents from Gunosy.'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('blog_id', nargs='+', type=int)

    def handle(self, *args, **options):
        print('ScrapeArticles command is called.')
