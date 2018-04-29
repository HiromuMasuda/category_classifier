"""gunosy article classification
category classification function from gunosy article url
"""

from django.core.management.base import BaseCommand
from classification_machine.models import Article
from classification_machine.modules.gunosy_article_scraper import (
        GunosyArticleScraper
        )
from classification_machine.static import consts
import pickle
import re


class GunosyArticleClassifier:

    def __init__(self, url):
        self.url = url

    def check_url_validness(self):
        """check whether input url is valid and gunosy's

        Args:
            None

        Returns:
            Boolean: is valid or not
        """
        pattern = r"%(url)s/articles/\w{5}" % {"url": consts.GUNOSY_ROOT_URL}
        is_valid_url = re.match(pattern, self.url)
        return is_valid_url

    def classify(self, tfidf, clf_model):
        """classification process of predicting category from url

        Args:
            tfidf(str): fitted tfidf model
            clf_model(str): fitted classification model

        Returns:
            str: gunosy category name
        """
        scraper = GunosyArticleScraper(self.url)
        content = scraper.get_article_content()
        content = tfidf.transform([content])
        pred_category = clf_model.predict(content)
        pred_category = consts.GUNOSY_CATEGORIES_DICT[pred_category[0]]
        pred_category_name = pred_category['name']
        return pred_category_name
