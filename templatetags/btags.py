# -*- coding: utf-8 -*-
from django import template
from ..models import BookDB, BookSet
from ..helper import is_var, cut_array

register = template.Library()

@register.inclusion_tag('tags/book.html')
def book_render(db_url, book_id, mode='main', prefix = ''):
    """
    Get book and render book info
    two input variables type
    db_url/id  db_url/book(Output class)
    """
    if(book_id.__class__.__name__ == 'Output'):
        book = book_id
    else:
        book = BookDB.objects.get(url=db_url).get_book(book_id)
    return {'mode': mode, 'prefix': prefix, 'book': book, 'db_url': db_url}


@register.inclusion_tag('tags/bookset.html')
def bookset_render(bookset_name, mode='main', prefix='', lenght=0):
    """
    Render bookset
    """
    bookset = BookSet.objects.get(name = bookset_name)
    bookset.books = cut_array(bookset.books, lenght)
    return {'bookset': bookset, 'mode': mode, 'prefix': prefix}
    

@register.inclusion_tag('tags/bookset_list.html')
def bookset_list(mode='main', prefix=''):
    """
    Render bookset list
    """
    booksets = BookSet.objects.filter(view_me=True)
    return {'booksets': booksets, 'mode': mode, 'prefix': prefix}


@register.tag
def book_search(parser, token):
    return BookSearch(token)


class BookSearch(template.Node):
    def __init__(self, argv):
        self.argv=argv

    def __repr__(self):
        return "<BookSearchNode>"

    def render(self, context):
        argv = list(self.argv.split_contents())
        if argv[-2] == 'as':
            name = argv[-1]
            argv = argv[:-2]
        else:
            name = 'book_search'
        
        if len(argv) >=3:
            db = is_var(context, argv[1])
            query = is_var(context, argv[2])
        else:
            raise NotEnoughValues('Set db_url and query')
            
        if len(argv) >=4:
            query_type = is_var(context, argv[3])
        else:
            query_type = 'PQF'
        
        books = BookDB.objects.get(url=db).query(query_type, query)
        if isinstance(books, basestring):
             result_len = 0
        else:
             result_len = len(books)

        if len(argv) == 5:
            lenght = is_var(context, argv[4])
            books = cut_array(books, lenght)
            
        if len(argv) == 6:
            start = is_var(context, argv[4])
            lenght = is_var(context, argv[5])
            books = books[start: start+lenght]
            
        context[name] = books
        context[name+'_len'] = result_len
        return ''
