# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from forms import QueryForm
from models import BookDB, BookSet
from PyZ3950 import zoom, zmarc


def query(request, **kwargs):
    if request.method == 'GET' and len(request.GET) > 0:
        form = QueryForm(request.GET)
        if form.is_valid(): 
            db=form.cleaned_data['db']
            db.encoding_in = form.cleaned_data['charset_in']
            db.encoding_out = form.cleaned_data['charset_out']
            db.syntax = form.cleaned_data['syntax']
            books = db.query(form.cleaned_data['query_type'], form.cleaned_data['query'])
            b_len = len(books)
    else:
        form = QueryForm()
    return render_to_response(kwargs['tpl'], locals())


def get_book(request, **kwargs):
    db = get_object_or_404(BookDB, url = kwargs['db_url'])
    if kwargs.has_key('debug'):
        server_address = db.host
        server_port = db.port
        db_name = db.db
        syntax = 'RUSMARC'
        q_type = 'pqf'
        query = '@attr 1=1035 "' + kwargs['id'].encode('utf-8', 'backslashreplace') + '"'
        conn = zoom.Connection (server_address, server_port, databaseName=db_name, preferredRecordSyntax=syntax)
        res = conn.search(zoom.Query (q_type, query))
        res_len = len(res)
        raw_data = str(res[0].data).decode(db.encoding_out)
        praw_data = str(zmarc.MARC(res[0].data, strict = 0)).decode(db.encoding_out)
        fields_array = str(zmarc.MARC(MARC=res[0].data, strict = 0).fields).decode(db.encoding_out)
        xml_data = str(zmarc.MARC(MARC=res[0].data, strict = 0).toMARCXML()).decode(db.encoding_out)
    else:
        search = db.connect()
        book = search.get_book(kwargs['id'].encode('utf-8', 'backslashreplace'))
        if book:
            book = book[0]
    return render_to_response(kwargs['tpl'], locals())
