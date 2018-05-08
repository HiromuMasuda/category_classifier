from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from classification_machine.models import *
from classification_machine.modules.gunosy_article_scraper import *
from classification_machine.modules.gunosy_article_classifier import *


class SearchFormView(TemplateView):
    template_name = "search_form.html"

    def __init__(self):
        with open(TFIDF_FILE_PATH, 'rb') as f:
            self.tfidf = pickle.load(f)
        with open(CLF_MODEL_FILE_PATH, 'rb') as f:
            self.clf_model = pickle.load(f)

    def get(self, request, *args, **kwargs):
        context = super(SearchFormView, self).get_context_data(**kwargs)

        url = request.GET.get('url', '')
        context['url'] = url
        classifier = GunosyArticleClassifier(url)
        is_valid_url = classifier.check_url_validness()

        if len(url) == 0:
            pass
        elif is_valid_url:
            try:
                pred_category_name = classifier.classify(
                        self.tfidf, self.clf_model)
                context['ans_msg'] = "カテゴリは「{}」です。".format(pred_category_name)
            except UrlInvalidError:
                context['error_msg'] = 'ページが見つかりません。'
        else:
            context['error_msg'] = '正しい記事URLを入力してください。'

        return render(self.request, self.template_name, context)
