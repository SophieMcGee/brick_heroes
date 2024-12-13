from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    """ A view to return the index page """
    return render(request, 'home/index.html')

@login_required
def profile(request):
    return render(request, 'home/profile.html')

def collections(request):
    return render(request, 'home/collections.html')