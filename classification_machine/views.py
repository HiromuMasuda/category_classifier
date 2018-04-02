from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from classification_machine.models import *
from janome.tokenizer import Tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import requests
import random
import pickle

class SearchFormView(TemplateView):
    template_name = "search_form.html"

    def get(self, request, *args, **kwargs):
        context = super(SearchFormView, self).get_context_data(**kwargs)

        url = request.GET.get('url', '')
        context['url'] = url

        # IMPROVE:
        # URLに対するバリデーション
        # Timeoutや404に対する対応

        # gunosyの記事リンクからcontents持ってくる処理は共通化しておきたい
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")

        contents = soup.find('div', class_='article gtm-click').find_all('p')
        content = ''
        for c in contents:
            content += c.text

        vectorizer = pickle.load(open('./vectorizer.sav', 'rb'))
        content = vectorizer.transform([content])

        clf = pickle.load(open('./model.sav', 'rb'))
        pred_category = clf.predict(content)

        category_list = {
                1: 'エンタメ',
                2: 'スポーツ',
                3: 'おもしろ',
                4: '国内',
                5: '海外',
                6: 'コラム',
                7: 'IT・科学',
                8: 'グルメ',
        }
        context['category'] = category_list[pred_category[0]]

        return render(self.request, self.template_name, context)
