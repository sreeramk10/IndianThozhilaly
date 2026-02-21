from magazine.models import SiteVisit

def visitor_count(request):
    return {
        'total_visits': SiteVisit.get_total_visits(),
    }