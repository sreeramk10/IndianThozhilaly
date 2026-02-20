from django.shortcuts import render
from magazine.models import SiteVisit, Magazine, Content

# Create your views here.

def visitor_count(request):
    return {
        'total_visits': SiteVisit.get_total_visits(),
    }