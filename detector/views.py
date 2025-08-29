# \pothole_project_django\detector\views.py

from django.shortcuts import render

def index(request):
    """Renders the main dashboard page."""
    return render(request, 'detector/index.html')