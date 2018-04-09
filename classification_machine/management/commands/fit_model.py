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

        train_X, test_X, train_y, test_y = train_test_split(
                docs, labels, test_size=0.2, random_state=0)

        print("train_X:", len(train_X), "test_X:", len(test_X))

        # tfidf
        tfidf = Tfidf()
        # tfidf = TfidfVectorizer()
        time_s = time.time()
        train_X = tfidf.fit_transform(train_X)
        test_X = tfidf.transform(test_X)

        time_e = time.time() - time_s
        print("time: {}m{}s".format(int(time_e // 60), int(time_e % 60)))

        # naive beyes
        nb = NaiveBayes()
        # nb = MultinomialNB(alpha=0.1, fit_prior='True')
        nb.fit(train_X, train_y)
        score = nb.score(test_X, test_y)
        print(score)

        # save learned models
        pickle.dump(nb, open('./nb.sav', 'wb'))
        pickle.dump(tfidf, open('./tfidf.sav', 'wb'))
