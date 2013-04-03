from django.http import HttpResponse
from django.shortcuts import render
from tfidf.search import rank, search_term
import json

def index(request):
    query = request.GET.get('query')
    context = None
    if query:
        context = {'docs': rank(query), 'query': query}
    return render(request, 'tfidf/home.html', context)

def term_autocomplete(request):
    term = request.GET.get('query')
    suggested_terms = search_term(term)
    result = {}
    result['suggestions'] = suggested_terms
    return HttpResponse(json.dumps(result))