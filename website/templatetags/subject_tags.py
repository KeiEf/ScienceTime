# website/templatetags/subject_tags.py
from django import template
from ..models import Subject

register = template.Library()

@register.simple_tag
def get_all_subjects():
    """Clean version - returns all subjects"""
    return Subject.objects.all()

@register.simple_tag
def get_subjects_with_fields():
    """
    Returns only subjects that have at least one related field
    """
    return Subject.objects.filter(field__isnull=False).distinct().order_by('id')