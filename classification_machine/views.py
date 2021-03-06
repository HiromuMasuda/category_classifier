from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from classification_machine.models import *
from classification_machine.modules.gunosy_article_scraper import *
import pickle
import re


class SearchFormView(TemplateView):
    template_name = "search_form.html"

    def get(self, request, *args, **kwargs):
        context = super(SearchFormView, self).get_context_data(**kwargs)

        url = request.GET.get('url', '')
        context['url'] = url

        pattern = r"https://gunosy.com/articles/\w{5}"
        is_valid_url = re.match(pattern, url)

        if len(url) == 0:
            pass
        elif is_valid_url:
            try:
                scraper = GunosyArticleScraper(url)
                content = scraper.get_article_content()

                tfidf = pickle.load(open('./tfidf.sav', 'rb'))
                content = tfidf.transform([content])

                clf_model = pickle.load(open('./clf_model.sav', 'rb'))
                pred_category = clf_model.predict(content)

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
                out_category = category_list[pred_category[0]]
                context['ans_msg'] = "カテゴリは「{}」です。".format(out_category)
            except UrlInvalidError:
                context['error_msg'] = 'ページが見つかりません。'
        else:
            context['error_msg'] = '正しい記事URLを入力してください。'

        return render(self.request, self.template_name, context)
