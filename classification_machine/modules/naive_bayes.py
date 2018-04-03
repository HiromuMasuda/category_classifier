from collections import defaultdict, Counter
import math


class NaiveBayes:

    def __init__(self):
        self.tokens      = set() # 重複なしの語彙
        self.cats        = set() # 重複なしのカテゴリ
        self.cat_count   = {}    # カテゴリの出現回数, {category : { words : n, ...}}
        self.token_count = {}    # カテゴリ毎の単語出現回数, {category : n}

    def train(self, docs, cats):
        self.tokens = set([item for sublist in docs for item in sublist])
        self.cats = set(cats)
        self.cat_count = Counter(cats)

        for cat in self.cats:
            self.token_count[cat] = defaultdict(lambda: 0)
        for doc_i, doc in enumerate(docs):
            cat = cats[doc_i]
            for token in doc:
                self.token_count[cat][token] += 1

    def word_probability(self, token, cat):
        '''単語が与えられた時のカテゴリである確率, P(word|cat)'''
        word_count = self.token_count[cat][token] + 1 # ラプラススムージング
        voc_count = sum(self.token_count[cat].values()) + len(self.tokens)
        return float(word_count) / float(voc_count)


    def score(self, doc, cat):
        '''文書(単語)が与えられたときのカテゴリである確率'''
        doc_count = sum(self.cat_count.values())
        score = math.log(float(self.cat_count[cat]) / doc_count)

        for token in docs:
            score += math.log(self.word_probability(token, cat))
        return score * (-1)


    def classify(self, doc):
        '''P(cat|doc)が最も大きなカテゴリを返す'''
        best  = None
        value = 0

        for cat in self.cats:
            v = self.score(doc, cat)
            if v > value:
                best  = cat
                value = v
        return best
