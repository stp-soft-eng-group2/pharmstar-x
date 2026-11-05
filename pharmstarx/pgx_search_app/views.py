from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def pgx_search_app(request):
    template = loader.get_template('pgx_search.html')
    return HttpResponse(template.render())
