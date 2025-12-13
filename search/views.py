from django.shortcuts import render
from django.views.generic import ListView

from products.models import Product


# Create your views here.


class SearchView(ListView):
    model = Product
    template_name = 'search.html'
    context_object_name = 'results'

    def get_queryset(self):
        results = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = results.filter(title__icontains=query)
            results = postresult
        else:
            results = None
        return results

