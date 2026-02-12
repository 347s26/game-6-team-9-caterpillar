from django.shortcuts import render
from django.views import generic

def index(request):
    """View function for home page of site."""
    return render(request, 'index.html', context=context)
