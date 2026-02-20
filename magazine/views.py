from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from magazine.models import Magazine, SiteVisit
from magazine.models import SiteVisit, Magazine, Content
from django.http import FileResponse, Http404
import os

# Create your views here.

def visitor_count(request):
    return {
        'total_visits': SiteVisit.get_total_visits(),
    }
    



def get_page_range(paginator, current_page, delta=2):
    pages = []
    last_added = None

    for num in paginator.page_range:
        is_boundary = (num == 1 or num == paginator.num_pages)
        is_near_current = (current_page - delta <= num <= current_page + delta)

        if is_boundary or is_near_current:
            if last_added is not None and num - last_added > 1:
                pages.append(None)
            pages.append(num)
            last_added = num

    return pages


def index(request):
    """Homepage with featured magazine, recent stories, and archive preview"""

    featured_magazine = Magazine.objects.filter(
        is_published=True,
        is_featured=True
    ).first()

    if not featured_magazine:
        featured_magazine = Magazine.objects.filter(
            is_published=True
        ).first()

    recent_magazines = Magazine.objects.filter(
        is_published=True
    ).exclude(
        id=featured_magazine.id if featured_magazine else None
    )[:6]

    archive_magazines = Magazine.objects.filter(
        is_published=True
    )[7:11]

    context = {
        'featured_magazine': featured_magazine,
        'recent_magazines': recent_magazines,
        'archive_magazines': archive_magazines,
    }
    return render(request, 'index.html', context)


def magazine_detail(request, slug):
    """Individual magazine detail page"""

    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    magazine.increment_view_count()

    related_magazines = Magazine.objects.filter(
        is_published=True
    ).exclude(id=magazine.id)[:3]

    context = {
        'magazine': magazine,
        'related_magazines': related_magazines,
    }
    return render(request, 'magazine_detail.html', context)


def archive(request):

    all_magazines = Magazine.objects.filter(
        is_published=True
    ).order_by('-issued_at')

    # 10 per page
    paginator = Paginator(all_magazines, 10)
    page = request.GET.get('page', 1)

    try:
        paginated_magazines = paginator.page(page)
    except PageNotAnInteger:
        paginated_magazines = paginator.page(1)
    except EmptyPage:
        paginated_magazines = paginator.page(paginator.num_pages)

    # Group current page items by year → list of (year, [magazines]) tuples
    year_dict = {}
    for magazine in paginated_magazines:
        if magazine.issued_at:
            year = magazine.issued_at.year
            if year not in year_dict:
                year_dict[year] = []
            year_dict[year].append(magazine)

    magazines_by_year = [
        (year, year_dict[year])
        for year in sorted(year_dict.keys(), reverse=True)
    ]

    context = {
        'paginated_magazines': paginated_magazines,
        'magazines_by_year': magazines_by_year,
        'page_range': get_page_range(paginator, paginated_magazines.number),
        'total_count': all_magazines.count(),
        'total_years': Magazine.objects.filter(
            is_published=True
        ).dates('issued_at', 'year').count(),
    }
    return render(request, 'archive.html', context)

def download_pdf(request, slug):
    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    if magazine.pdf and os.path.exists(magazine.pdf.path):
        response = FileResponse(
            open(magazine.pdf.path, 'rb'),
            content_type='application/pdf'
        )
        response['Content-Disposition'] = (
            f'attachment; filename="{os.path.basename(magazine.pdf.name)}"'
        )
        return response
    raise Http404

def developers(request):
    return render(request, "developers.html")