from collections import defaultdict, Counter
import math
import numpy as np

"""
P(cat|doc): proberbility of cat when doc is given.

=  P(cat)P(doc|cat) / P(doc)
=: P(cat)P(doc|cat)
=: P(cat)ΠP(wordk|cat)
=: logP(cat) + ΣlogP(wordk|cat)
"""

class NaiveBayes:

    def __init__(self):
        self.cats        = set() # (1,2,3,4,5,6,7,8)
        self.cat_count   = {}    # {1: 40, 2: 38, 3: 50 ...}
        self.token_scores = {}   # {1: [3.30, 1.25, 0, 0, 4.33, 0], 2: [] ...}

    def train(self, docs, cats):
        self.cats = set(cats)
        self.cat_count = Counter(cats)

        for c in self.cats:
            indexes = [i for i,cat in enumerate(cats) if cat == c]
            cat_docs = np.array(list(docs[i] for i in indexes))
            sum_cat_docs = cat_docs.sum(axis=0)
            self.token_scores[c] = sum_cat_docs

    def score(self, doc, cat):
        '''P(cat|doc) =: logP(cat) + ΣlogP(wordk|cat)'''
        '''文書(単語)が与えられたときのカテゴリである確率'''

        # これ共通だから使いまわしたい
        doc_count = sum(self.cat_count.values())
        cat_doc_count = self.cat_count[cat]
        p_cat = math.log(float(cat_doc_count) / doc_count) * (-1)

        doc_cat_sum_score = doc.multiply(self.token_scores[cat])
        doc_cat_sum_score = np.log(doc_cat_sum_score.toarray() + 1)
        doc_cat_score     = doc_cat_sum_score.sum()

        score = p_cat + doc_cat_score
        return score

    def classify(self, doc):
        '''P(cat|doc)が最も大きなカテゴリを返す'''
        cat_scores = {}

        for cat in self.cats:
            score = self.score(doc, cat)
            cat_scores[cat] = score

        pred_cat = max(cat_scores.items(), key=lambda x: x[1])[0]
        return pred_cat






