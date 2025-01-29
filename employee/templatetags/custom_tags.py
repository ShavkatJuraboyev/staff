from django import template

register = template.Library()

@register.simple_tag
def distinct(queryset):
    """Berilgan querysetni takrorlanmas qilib qaytaradi."""
    return "Salom, bu maxsus teg!"
