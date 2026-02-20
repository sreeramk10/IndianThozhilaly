from magazine.models import SiteVisit

class VisitorCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('has_visited', False):
            SiteVisit.objects.create()
            request.session['has_visited'] = True
            request.session.set_expiry(86400)
        
        response = self.get_response(request)
        return response