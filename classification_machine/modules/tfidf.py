# from django.core.management.base import BaseCommand
# from classification_machine.models import *

import math
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter, RegexReplaceCharFilter
from janome.tokenfilter import POSStopFilter

import numpy as np


class Tfidf:

    def __init__(self):
        pass

    def fit_transform(self, docs):
        return self.tfidf(docs)

    def tf(self, token, tokenized_doc):
        return tokenized_doc.count(token)

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

        # ここ計算がやばい、大量データに対応できない
        for doc in tokenized_docs:
            doc_tfidf = []
            for term in idf.keys():
                tf = self.tf(term, doc)
                doc_tfidf.append(tf * idf[term])
            tfidf_docs.append(doc_tfidf)
        return tfidf_docs

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
