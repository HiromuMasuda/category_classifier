from django.core.management.base import BaseCommand
from classification_machine.models import *

import math
import numpy as np
import pandas as pd
from scipy import sparse
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter, RegexReplaceCharFilter
from janome.tokenfilter import POSStopFilter


class Tfidf:

    def __init__(self):
        pass

    def fit_transform(self, docs):
        return self.tfidf(docs)

    def tf(self, tokenized_doc):
        tokenized_doc = np.array(tokenized_doc)
        unique, counts = np.unique(tokenized_doc, return_counts=True)
        return dict(zip(unique, counts))

    def idf(self, tokenized_docs):
        idf_values = {}
        all_tokens_set = set([item for sublist in tokenized_docs for item in sublist])
        tokenized_docs_len = len(tokenized_docs)
        for token in all_tokens_set:
            contains_token = map(lambda doc: token in doc, tokenized_docs)
            idf_values[token] = 1 + math.log(tokenized_docs_len/(sum(contains_token)))
        return idf_values

    def tfidf(self, docs):
        tokenized_docs = [self.tokenize(doc) for doc in docs]
        idf = self.idf(tokenized_docs)
        tfidf_docs = []

        for doc in tokenized_docs:
            tf = self.tf(doc)
            out = [v*tf[k] if k in tf else 0 for k, v in idf.items()]
            tfidf_docs.append(out)
        return sparse.lil_matrix(tfidf_docs)

    def tokenize(self, doc):
        tokenizer = Tokenizer()
        analyzer = Analyzer(self.char_filters(), tokenizer, self.token_filters())
        return [token.surface for token in analyzer.analyze(doc)]

    def char_filters(self):
        char_filters = [
                UnicodeNormalizeCharFilter(),
                RegexReplaceCharFilter("[,\.\(\)\{\}\[\]]"," "),
                RegexReplaceCharFilter("\d", " ")
        ]
        return char_filters

    def token_filters(self):
        ignore_filter=['接続詞', '接頭辞', '接尾辞', '記号', '助詞', '助動詞']
        token_filters = [POSStopFilter(ignore_filter)]
        return token_filters
