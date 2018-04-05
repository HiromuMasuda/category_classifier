from django.core.management.base import BaseCommand
from classification_machine.models import *
from classification_machine.modules.naive_bayes import *

import glob
import random
from sklearn.model_selection import train_test_split
from janome.tokenizer import Tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
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


        nb = NaiveBayes()
        nb.train(train_X, train_y)

        acc_count = 0
        total_test_len = len(test_y)
        for i in range(total_test_len):
            pred_y = nb.classify(test_X[i])
            if pred_y == test_y[i]:
                acc_count += 1

        print("acc: {}%".format(acc_count*100/total_test_len, '%'))

        # # Make this logic from scratch.
        # clf = MultinomialNB(alpha=0.1, fit_prior='True')
        # clf.fit(train_X, train_y)
        #
        # # save learned models
        # pickle.dump(clf, open('./model.sav', 'wb'))
        # pickle.dump(vectorizer, open('./vectorizer.sav', 'wb'))
