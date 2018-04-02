from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from classification_machine.models import *
from janome.tokenizer import Tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import requests
import random
import pickle
import re

class SearchFormView(TemplateView):
    template_name = "search_form.html"

    def get(self, request, *args, **kwargs):
        context = super(SearchFormView, self).get_context_data(**kwargs)

        url = request.GET.get('url', '')
        context['url'] = url

        pattern = r"https://gunosy.com/articles/\w{5}"
        is_valid_url = re.match(pattern , url)

        if is_valid_url:
            try:
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

                # enumとi18nをうまく使いたい
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
            except AttributeError: # 404
                context['error_msg'] = 'ページが見つかりません。'
            except: # other errors
                context['error_msg'] = 'エラーが発生しました。'
        else:
            context['error_msg'] = '正しい記事URLを入力してください。'

        return render(self.request, self.template_name, context)
