from django.core.management.base import BaseCommand
from classification_machine.models import *
from classification_machine.modules.tfidf import *
from classification_machine.modules.naive_bayes import *

from sklearn.model_selection import train_test_split
from janome.tokenizer import Tokenizer
import pickle

# for debug
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

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

        # tfidf : lib
        # vectorizer = TfidfVectorizer()
        # train_X = vectorizer.fit_transform(train_X)
        # test_X = vectorizer.transform(test_X)

        # tfidf : scratch
        train_len, test_len = 100, 10
        tfidf = Tfidf()
        train_X = tfidf.fit_transform(train_X[:train_len]) # takes 95% of time
        test_X  = tfidf.transform(test_X[:test_len])
        train_y = train_y[:train_len]
        test_y  = train_y[:test_len]

        # NaiveBayes : lib
        # nb = MultinomialNB(alpha=0.1, fit_prior='True')
        # nb.fit(train_X, train_y)
        # score = nb.score(test_X, test_y)
        # print(score)

        # NaiveBayes : scratch
        nb = NaiveBayes()
        nb.fit(train_X, train_y)
        score = nb.score(test_X, test_y)
        print(score)

        # save learned models
        pickle.dump(nb, open('./nb.sav', 'wb'))
        pickle.dump(tfidf, open('./tfidf.sav', 'wb'))
