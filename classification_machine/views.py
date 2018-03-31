from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from classification_machine.models import *

class SearchFormView(TemplateView):
    template_name = "search_form.html"

    def get(self, request, *args, **kwargs):
        context = super(SearchFormView, self).get_context_data(**kwargs)
        return render(self.request, self.template_name, context)
