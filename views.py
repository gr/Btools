# -*def coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from ZClient.ZClient import ZClient
from PyZ3950 import zoom, zmarc
from django.conf import settings
from models import BookSet
'''
in   **kwargs:
        -db name
        -book id
        -template name
     request:
        -
        -
out: book:
        -
'''
def get_book(request, **kwargs):
    search = ZClient()
    page='book'
    if kwargs.has_key('db'):
        db = kwargs['db']
    else:
        db = settings.Z3950_DB
    search.connect(settings.Z3950_HOST,
                   settings.Z3950_PORT,
                   db,
                   settings.Z3950_SYNTAX,
                   settings.Z3950_CHARSET)
    book = search.get_book(kwargs['id'])
    if book:
        book = book[0]
        if kwargs.has_key('debug'):
            server_address = settings.Z3950_HOST
            server_port = settings.Z3950_PORT
            db_name = db
            syntax = settings.Z3950_SYNTAX
            q_type = 'pqf'
            query = '@attr 1=12 "' + str(int(kwargs['id'])) + '"'
            conn = zoom.Connection (server_address, server_port, databaseName=db_name, preferredRecordSyntax=syntax)
            res = conn.search(zoom.Query (q_type, query))
            res_len = len(res)
            raw_data = str(res[0].data).decode(settings.Z3950_CHARSET)
            praw_data = str(zmarc.MARC(res[0].data)).decode(settings.Z3950_CHARSET)
            fields_array = str(zmarc.MARC(MARC=res[0].data).fields).decode(settings.Z3950_CHARSET)
            xml_data = str(zmarc.MARC(MARC=res[0].data).toMARCXML()).decode(settings.Z3950_CHARSET)
    return render_to_response(kwargs['tpl'], locals())

'''
in: request:
        -
out: books - array of books
     b_len - 
'''
def query(request, **kwargs):
    search = ZClient()
    db_name = request.GET.get('db_name', 'books')
    search.connect(settings.Z3950_HOST,
                   settings.Z3950_PORT,
                   db_name,
                   settings.Z3950_SYNTAX,
                   settings.Z3950_CHARSET)
    query_ = request.GET.get('query', 'london').strip()
    type_ = request.GET.get('type', 'ccl')
    books, b_len = search.query(query_type=type_, query=query_, length=1000)
    return render_to_response(kwargs['tpl'], locals())


def bookset_index(request, **kwargs):
    booksets = BookSet.objects.all()
    return render_to_response(kwargs['tpl'], locals())


def bookset(request, **kwargs):
    if kwargs.has_key('bookset'):
        bookset = get_object_or_404(BookSet, name=kwargs['bookset'])
    return render_to_response(kwargs['tpl'],  locals())
