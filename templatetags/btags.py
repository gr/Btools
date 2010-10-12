# -*- coding: utf-8 -*-
from django import template

register = template.Library()

@register.inclusion_tag('book.html')
def book_render(book):
    return {'book': book}
