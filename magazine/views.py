from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from magazine.models import Magazine, SiteVisit, Content
from django.http import FileResponse, Http404
import os


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
    featured_magazine = Magazine.objects.filter(
        is_published=True,
        is_featured=True
    ).first()

    if not featured_magazine:
        featured_magazine = Magazine.objects.filter(
            is_published=True
        ).first()

    # Fetch contents from published magazines for stories grid
    recent_contents = Content.objects.filter(
        magazine__is_published=True
    ).select_related('magazine').order_by(
        '-magazine__issued_at', 'page_number'
    )[:6]

    archive_magazines = Magazine.objects.filter(
        is_published=True
    )[7:11]

    context = {
        'featured_magazine': featured_magazine,
        'recent_contents': recent_contents,
        'archive_magazines': archive_magazines,
    }
    return render(request, 'index.html', context)



def magazine_detail(request, slug):
    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    magazine.increment_view_count()

    # Fetch all sub-PDF contents ordered by page number
    contents = magazine.content.all()

    context = {
        'magazine': magazine,
        'contents': contents,
    }
    return render(request, 'magazine_detail.html', context)


def archive(request):
    all_magazines = Magazine.objects.filter(
        is_published=True
    ).order_by('-issued_at')

    paginator = Paginator(all_magazines, 10)
    page = request.GET.get('page', 1)

    try:
        paginated_magazines = paginator.page(page)
    except PageNotAnInteger:
        paginated_magazines = paginator.page(1)
    except EmptyPage:
        paginated_magazines = paginator.page(paginator.num_pages)

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
