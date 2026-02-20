from django.utils.text import slugify as django_slugify
from slugify import slugify as latin_slugify  # from python-slugify
from django.db.models import Model

def generate_unique_slug(instance: Model, value: str, field_name: str = "slug", transliterate: bool = False):
    """
    Generate a unique slug for a given model instance.
    
    :param instance: The model instance
    :param value: The text to slugify (e.g., title)
    :param field_name: The slug field name in the model
    :param transliterate: If True, transliterate to Latin; if False, keep Unicode
    """
    if transliterate:
        base_slug = latin_slugify(value)
    else:
        base_slug = django_slugify(value, allow_unicode=True)

    slug = base_slug
    counter = 1
    ModelClass = instance.__class__

    while ModelClass.objects.filter(**{field_name: slug}).exclude(pk=instance.pk).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug