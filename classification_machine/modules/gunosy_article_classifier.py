"""gunosy article classification
category classification function from gunosy article url
"""

from django.core.management.base import BaseCommand
from classification_machine.models import *
from classification_machine.modules.gunosy_article_scraper import *
from classification_machine.static.consts import *
import pickle
import re


class GunosyArticleClassifier:

    def __init__(self, url):
        self.url = url

    def check_url_validness(self):
        pattern = r"%(root_url)s/articles/\w{5}" % {"root_url": GUNOSY_ROOT_URL}
        is_valid_url = re.match(pattern, self.url)

        return is_valid_url

    def get_category_name(self):
        pred_category = self.classify()
        pred_category_name = CATEGORY_NAME_JP_DIC[pred_category[0]]

        return pred_category_name

    def classify(self):
        scraper = GunosyArticleScraper(self.url)
        content = scraper.get_article_content()

        tfidf = pickle.load(open(TFIDF_FILE_PATH, 'rb'))
        content = tfidf.transform([content])

        clf_model = pickle.load(open(CLF_MODEL_FILE_PATH, 'rb'))
        pred_category = clf_model.predict(content)

        return pred_category

