from django.shortcuts import render


# Define the index view
def index(request):
    """
    Renders the index page.
    """
    return render(request, 'pages/index.html')

# Define the about view
def about(request):
    """
    Renders the about page.
    """
    return render(request, 'pages/about.html')
