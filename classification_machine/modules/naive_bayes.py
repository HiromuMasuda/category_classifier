from collections import Counter
import math
import numpy as np


class NaiveBayes:

    def __init__(self):
        self.cats = set()  # (1,2,3,4,5,6,7,8)
        self.cat_count = {}    # {1: 40, 2: 38, 3: 50 ...}
        self.token_scores = {}    # {1: [3.30, 1.25, 0, 0, 4.33, 0], 2: [] ...}
        self.cat_probs = {}

    def fit(self, docs, cats):
        self.cats = set(cats)
        self.cat_count = Counter(cats)

        for c in self.cats:
            # self.token_scores
            indexes = [i for i, cat in enumerate(cats) if cat == c]
            cat_docs = np.array(list(docs[i] for i in indexes))
            sum_cat_docs = cat_docs.sum(axis=0)
            self.token_scores[c] = sum_cat_docs

            # self.cat_probs
            doc_count = sum(self.cat_count.values())
            cat_doc_count = self.cat_count[c]
            p_cat = math.log(float(cat_doc_count) / doc_count) * (-1)
            self.cat_probs[c] = p_cat

    def predict(self, doc):
        # return the category which P(cat|doc) is the biggest
        cat_scores = {}
        for cat in self.cats:
            score = self.get_cat_score(doc, cat)
            cat_scores[cat] = score

        pred_cat = max(cat_scores.items(), key=lambda x: x[1])[0]
        return pred_cat

    def score(self, docs, cats):
        acc_count = 0
        total_len = len(cats)
        for i in range(total_len):
            pred = self.predict(docs[i])
            if pred == cats[i]:
                acc_count += 1

        score = acc_count / total_len
        return score

    def get_cat_score(self, doc, cat):
        # P(cat|doc) =: logP(cat) + ΣlogP(wordk|cat)
        # the prob of category when doc is given
        doc_cat_sum_score = doc.multiply(self.token_scores[cat])
        doc_cat_sum_score = np.log(doc_cat_sum_score.toarray() + 1)
        doc_cat_score = doc_cat_sum_score.sum()

        score = self.cat_probs[cat] + doc_cat_score
        return score
