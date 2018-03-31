from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from classification_machine.models import *
# from classification_machine.forms import UrlForm
import random

class SearchFormView(TemplateView):
    template_name = "search_form.html"

    def get(self, request, *args, **kwargs):
        context = super(SearchFormView, self).get_context_data(**kwargs)

        context['url'] = request.GET.get('url', '')

        # モデルに突っ込んで得られた結果を返す
        out_category = random.choice(['エンタメ', 'おもしろ', 'IT・科学', 'グルメ'])
        context['category'] = out_category

        return render(self.request, self.template_name, context)
