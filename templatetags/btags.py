# -*- coding: utf-8 -*-
from django import template
from ..models import BookDB, BookSet

register = template.Library()

@register.inclusion_tag('tags/book.html')
def book_render(db_url, book_id):
    """
    Get book and render book info
    """
    search = BookDB.objects.get(url=db_url).connect()
    book = search.get_book(book_id)
    if book:
        book = book[0]
    return {'book': book, 'db_url': db_url}


@register.inclusion_tag('tags/bookset.html')
def bookset_render(bookset_name): #name, type, len, pagination, from begin/end
    """
    Render bookset
    """
    bookset = BookSet.objects.get(name=bookset_name)
    return {'bookset': bookset}
    

@register.inclusion_tag('tags/bookset_list.html')
def bookset_list():
    """
    Render bookset list
    """
    booksets = BookSet.objects.all()
    return {'booksets': booksets}
