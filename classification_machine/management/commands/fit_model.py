from django.core.management.base import BaseCommand
from classification_machine.models import *


class Command(BaseCommand):
    help = 'Fit article_classification model.'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('blog_id', nargs='+', type=int)

    def handle(self, *args, **options):
        print('FitModel command is called.')
