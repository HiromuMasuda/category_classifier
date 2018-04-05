from django.core.management.base import BaseCommand
from classification_machine.models import *
from classification_machine.modules.naive_bayes import *
from sklearn.model_selection import train_test_split
from janome.tokenizer import Tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


class Command(BaseCommand):
    help = 'Fit article_classification model.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        docs = []
        labels = []
        for article in Article.objects.all():
            docs.append(article.content)
            labels.append(article.category)

        train_X, test_X, train_y, test_y = \
                train_test_split(docs, labels, test_size=0.2, random_state=0)

        # Make this logic from scratch.
        vectorizer = TfidfVectorizer()
        train_X = vectorizer.fit_transform(train_X)
        test_X = vectorizer.transform(test_X)

        # Made NaiveBayes logic from scratch.
        nb = NaiveBayes()
        nb.fit(train_X, train_y)
        score = nb.score(test_X, test_y)
        print(score)

        # # save learned models
        pickle.dump(nb, open('./model.sav', 'wb'))
        pickle.dump(vectorizer, open('./vectorizer.sav', 'wb'))
