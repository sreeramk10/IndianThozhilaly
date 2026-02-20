"""
All models.

"""

import random
import uuid
from django.db import models
from django.utils import timezone
from magazine.utils.slug import generate_unique_slug

# Create your models here.
"""
Magazine models.

"""


class Magazine(models.Model):
    id = models.CharField(
        max_length=20, primary_key=True, editable=False, verbose_name="ID"
    )
    title = models.CharField(max_length=500, verbose_name="Title")
    cover_image = models.ImageField(
        upload_to="magazine/{id}/", null=True, blank=True, verbose_name="Cover Image"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    pdf = models.FileField(
        upload_to="magazine/{id}/pdf/", null=True, blank=True, verbose_name="PDF"
    )
    is_published = models.BooleanField(default=False, verbose_name="Published")
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Created At"
    )
    issued_at = models.DateField(blank=True, null=True, verbose_name="Issued At")
    page_count = models.IntegerField(blank=True, null=True, verbose_name="Page Count")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Magazine"
        verbose_name_plural = "Magazine"
        ordering = ["-created_at"]

    def __str__(self):
        if len(self.title) > 50:
            return f"{self.title[50]}..."
        return self.title

    # Generate ID
    def __generate_id(self):
        new_id = f"MAG{uuid.uuid4().hex[:8].upper()}{random.randint(100, 999)}"
        while True:
            try:
                Magazine.objects.get(id=new_id)
            except Magazine.DoesNotExist:
                return new_id

    def __change_issued_at(self):
        self.issued_at = timezone.now()
        if self.is_published:
            self.issued_at = timezone.now().date()
        if not self.is_published and self.issued_at is not None:
            self.issued_at = None

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.__generate_id()
        if not self.slug:
            if len(self.title) > 50:
                self.slug = generate_unique_slug(
                    self, self.title[:50], transliterate=True
                )
            self.slug = generate_unique_slug(self, self.title, transliterate=True)
        self.__change_issued_at()
        super(Magazine, self).save(*args, **kwargs)


"""
Content models.

"""


class Content(models.Model):
    magazine = models.ForeignKey(
        Magazine,
        on_delete=models.CASCADE,
        related_name="content",
        verbose_name="Magazine",
    )
    title = models.CharField(max_length=500, verbose_name="Title")
    page_number = models.IntegerField(verbose_name="Page Number")
    image = models.ImageField(
        upload_to="magazine/{magazine_id}/content/",
        null=True,
        blank=True,
        verbose_name="Content Image",
    )
    added_at = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Added At"
    )
    slug = models.SlugField(
        max_length=200, unique=True, verbose_name="Content Slug", editable=False
    )

    class Meta:
        verbose_name = "Content"
        verbose_name_plural = "Contents"
        ordering = ["page_number"]

    def __str__(self):
        return f"{self.title} (Page {self.page_number})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.title, transliterate=True)
        super(Content, self).save(*args, **kwargs)


"""
Site visit model to track the number of visits to the site.

"""


class SiteVisit(models.Model):
    visited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Site Visit"
        verbose_name_plural = "Site Visit"
        ordering = ["-visited_at"]

    @classmethod
    def get_total_visits(cls):
        return cls.objects.count()

    def __str__(self):
        return f"Visit at {self.visited_at}"
