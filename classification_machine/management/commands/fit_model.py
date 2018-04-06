from django.core.management.base import BaseCommand
from classification_machine.models import *
from classification_machine.modules.tfidf import *
from classification_machine.modules.naive_bayes import *

from sklearn.model_selection import train_test_split
from janome.tokenizer import Tokenizer
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

        # tf-idf
        # vectorizer = TfidfVectorizer()
        # train_X = vectorizer.fit_transform(train_X)
        # test_X = vectorizer.transform(test_X)
        tfidf = Tfidf()
        train_X = tfidf.fit_transform(train_X[:100])
        test_X  = tfidf.transform(test_X[:100])
        train_y = train_y[:10]
        test_y  = train_y[:10]

        # NaiveBayes
        # clf = MultinomialNB(alpha=0.1, fit_prior='True')
        # clf.fit(train_X, train_y)
        nb = NaiveBayes()
        nb.fit(train_X, train_y)
        score = nb.score(test_X, test_y)
        print(score)

        # save learned models
        pickle.dump(nb, open('./nb.sav', 'wb'))
        pickle.dump(tfidf, open('./tfidf.sav', 'wb'))
