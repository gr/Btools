# -*- coding: utf-8 -*-
from django import template
from ..models import BookDB, BookSet

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
        search = BookDB.objects.get(url=db_url).connect()
        book = search.get_book(book_id)
        if book:
            book = book[0]
    return {'mode': mode, 'prefix': prefix, 'book': book, 'db_url': db_url}


@register.inclusion_tag('tags/bookset.html')
def bookset_render(bookset_name, mode='main', prefix='', lenght=0):
    """
    Render bookset
    """
    bookset = BookSet.objects.get(name = bookset_name)
    try:
        lenght = int(lenght)
        if lenght > 0:
            bookset.books = bookset.books[:lenght]
        else:
            bookset.books = bookset.books[lenght:]
    except:
        pass
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
            
        is_var = lambda dict, key: dict[key] if dict.has_key(key) else key[1:-1]
        
        if len(argv) >=3:
            db = is_var(context, argv[1])
            query = is_var(context, argv[2])
        else:
            raise NotEnoughValues('Set db_url and query')
            
        if len(argv) >=4:
            query_type = is_var(context, argv[3])
        else:
            query_type = 'PQF'
            
        if len(argv) == 6:
            start = int(argv[4])
            lenght = int(argv[5])
        else:
            start = 0
            lenght = 100
        
            
        books = BookDB.objects.get(url=db).connect().query(query_type, query, start, lenght)
        context[name] = books[0]
        context[name+'_len'] = books[1]
        return ''
