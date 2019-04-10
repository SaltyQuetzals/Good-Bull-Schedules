from django.shortcuts import render

def index(request):
    """View function for home page of site."""
    print(request.user)
    return render(request, 'index.html')