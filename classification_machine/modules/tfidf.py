"""tf-idf model
This is the tf-idf model made from scratch.
"""

from django.core.management.base import BaseCommand
from classification_machine.models import *

import math
import numpy as np
import pandas as pd
import time
from scipy import sparse
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import POSKeepFilter
from janome.charfilter import (
        UnicodeNormalizeCharFilter,
        RegexReplaceCharFilter
        )


class Tfidf:

    def __init__(self):
        self.idf_docs_dic = {}

    def fit_transform(self, docs):
        """tf-idf fit & learning method

        Args:
            docs (list): list that made from row train document

        Returns:
            list: characterized docs
        """
        return self.tfidf(docs, fit=True)

    def transform(self, docs):
        """tf-idf learning method

        Args:
            docs (list): list that made from row test document

        Returns:
            list: characterized docs
        """
        return self.tfidf(docs, fit=False)

    def tf(self, tokenized_doc):
        """tf: term-frequency calculation

        Args:
            tokenized_doc (list): list of tokenized words

        Returns:
            dictionary: key: word, value: times that word appears in the doc
        """
        tokenized_doc = np.array(tokenized_doc)
        unique, counts = np.unique(tokenized_doc, return_counts=True)
        return dict(zip(unique, counts))

    def idf(self, tokenized_docs):
        """idf: inverse-document-frequency calculation

        Args:
            tokenized_docs (list): list of tokenized document

        Returns:
            dictionary: key: word, value: idf score of the word
        """
        idf_values = {}
        all_tokens_set = set(
                [item for sublist in tokenized_docs for item in sublist])
        tokenized_docs_len = len(tokenized_docs)
        for token in all_tokens_set:
            contains_token = map(lambda doc: token in doc, tokenized_docs)
            idf_values[token] = 1 + math.log(
                    tokenized_docs_len/(sum(contains_token)))
        return idf_values

    def tfidf(self, docs, fit):
        """tf-idf: tf-idf calculation of documents

        Args:
            docs (list): list of row document
            fit (Boolean): fit flag for train/test documents

        Returns:
            sparse matrix: list of tfidf scores
        """
        tokenized_docs = [self.tokenize(doc) for doc in docs]
        if fit:
            idf = self.idf(tokenized_docs)
            self.idf_docs_dic = idf
        else:
            idf = self.idf_docs_dic
        tfidf_docs = []

        for doc in tokenized_docs:
            tf = self.tf(doc)
            out = [v*tf[k] if k in tf else 0 for k, v in idf.items()]
            tfidf_docs.append(out)
        return sparse.lil_matrix(tfidf_docs)

    def tokenize(self, doc):
        """tokenize document

        Args:
            doc (str): row document

        Returns:
            list: tokenized words
        """
        tokenizer = Tokenizer()
        analyzer = Analyzer(
                self.char_filters(),
                tokenizer,
                self.token_filters())
        return [token.surface for token in analyzer.analyze(doc)]

    def char_filters(self):
        """char_filters for janome tokenizer

        Args:
            None

        Returns:
            list: char_filers
        """
        char_filters = [
                UnicodeNormalizeCharFilter(),
                RegexReplaceCharFilter("[,\.\(\)\{\}\[\]\:\-\"\'\@\!\?]", " "),
                RegexReplaceCharFilter("\d", " ")
        ]
        return char_filters

    def token_filters(self):
        """token_filters for janome tokenizer

        Args:
            None

        Returns:
            list: token_filers
        """
        keep_filter = ['名詞', '動詞']
        token_filters = [POSKeepFilter(keep_filter)]
        return token_filters
