"""fit_model
Custom command for fitting stored articles to model
command: python manage.py fit_model
"""

from django.core.management.base import BaseCommand
from classification_machine.models import Article
from classification_machine.modules.tfidf import Tfidf
from classification_machine.modules.naive_bayes import NaiveBayes
from sklearn.model_selection import train_test_split
import pickle

# classification
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier


class Command(BaseCommand):
    help = 'Fit article_classification model.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        N = 100
        print("N:", N)

        docs = []
        labels = []
        for article in Article.objects.all().order_by('?')[:N]:
            docs.append(article.title + " " + article.content)
            labels.append(article.category)

        train_X, test_X, train_y, test_y = train_test_split(
                docs, labels, test_size=0.2, random_state=0)

        print("train_X:", len(train_X), "test_X:", len(test_X))

        # tfidf
        tfidf = Tfidf()
        train_X = tfidf.fit_transform(train_X)
        test_X = tfidf.transform(test_X)

        # classification
        clf_models = {
                'my_naive_bayes': NaiveBayes(),
                'naive_bayes': MultinomialNB(),
                'sgd': SGDClassifier(),
                'k-neighbors': KNeighborsClassifier(),
                'logistic-reg': LogisticRegression(),
                'liner-svm': LinearSVC(),
                'random_forest': RandomForestClassifier(),
                'decision_tree': DecisionTreeClassifier()}
        clf_scores = {}
        best_clf = {'score': 0, 'model': None}

        for name, model in clf_models.items():
            model.fit(train_X, train_y)
            score = model.score(test_X, test_y)
            clf_scores[name] = score
            if best_clf['score'] < score:
                best_clf = {'score': score, 'model': model}

        for k, v in clf_scores.items():
            print("{}: {}".format(k, v))

        # save learned models
        pickle.dump(tfidf, open('./tfidf.sav', 'wb'))
        pickle.dump(best_clf['model'], open('./clf_model.sav', 'wb'))
