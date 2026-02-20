from django.utils import timezone
from django_daisy.mixins import NavTabMixin
from django.contrib import admin
from magazine.models import Magazine, Content, SiteVisit
from django.utils.html import format_html

# Register your models here.
admin.site.site_header = "THOZHILALY"
admin.site.site_title = "THOZHILALY"


class ContentInline(admin.TabularInline,NavTabMixin):
    model = Content
    fieldsets = (("Content Details", {"fields": ("title", "image", "c_pdf")}),)
    extra = 1


@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    inlines = [ContentInline]

    # Custom admin CSS for better styling
    class Media:
        css = {"all": ("css/admin/custom_admin.css",)}

    # Admin display for cover image preview and shortened title
    def image_preview(self, obj):
        if not obj.cover_image:
            return "No Image Uploaded"
        return format_html('<img src="{}" width="500" />', obj.cover_image.url)

    def shorterned_title(self, obj):
        if len(obj.title) > 50:
            return obj.title[:50] + "..."
        return obj.title

    image_preview.short_description = "Cover Image Preview"

    def make_published(self, request, queryset):
        queryset.update(is_published=True)
        queryset.update(issued_at=timezone.now().date())

    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)
        queryset.update(issued_at=None)

    def content_count(self, obj):
        return obj.content.count()

    content_count.short_description = "Number of Contents"

    list_display = (
        "shorterned_title",
        "is_published",
        "content_count",
        "issued_at",
        "created_at",
    )
    readonly_fields = ("image_preview", "slug", "issued_at", "created_at", "id", "view_count")
    list_display_links = ("shorterned_title",)
    list_filter = ("is_published", "created_at", "issued_at")
    list_per_page = 10
    search_fields = ("title", "description")
    actions = ["make_published", "make_unpublished"]
    fieldsets = (
        (
            "Magazine",
            {
                "fields": (
                    "title",
                    "description",
                )
            },
        ),
        (
            "Media",
            {
                "fields": (
                    "cover_image",
                    "image_preview",
                )
            },
        ),
        (
            "PDF & Details",
            {
                "fields": (
                    "pdf",
                    "page_count",
                )
            },
        ),
        
        (
            "Publication Options",
            {
                "fields": (
                    "is_published",
                    "issued_at",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "slug",
                    "created_at",
                    "id",
                    "view_count",
                )
            },
        ),
    )
    
