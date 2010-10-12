# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from forms import QueryForm
from models import BookDB
from ZClient import ZClient
from PyZ3950 import zoom, zmarc

def query(request, **kwargs):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid(): 
            search = ZClient()
            db=form.cleaned_data['db']
            search.connect(db.host,
                           db.port,
                           db.db,
                           form.cleaned_data['syntax'],
                           form.cleaned_data['charset'])
            books, b_len = search.query(form.cleaned_data['query_type'], form.cleaned_data['query'], 1000)
    else:
        form = QueryForm()
    return render_to_response(kwargs['tpl'], locals())


def get_book(request, **kwargs):
    db = BookDB
    db = db.objects.get(url=kwargs['db_url'])
    if kwargs.has_key('debug'):
        server_address = db.host
        server_port = db.port
        db_name = db.db
        syntax = 'RUSMARC'
        q_type = 'pqf'
        query = '@attr 1=12 "' + str(int(kwargs['id'])) + '"'
        conn = zoom.Connection (server_address, server_port, databaseName=db_name, preferredRecordSyntax=syntax)
        res = conn.search(zoom.Query (q_type, query))
        res_len = len(res)
        raw_data = str(res[0].data).decode(db.encoding)
        praw_data = str(zmarc.MARC(res[0].data)).decode(db.encoding)
        fields_array = str(zmarc.MARC(MARC=res[0].data).fields).decode(db.encoding)
        xml_data = str(zmarc.MARC(MARC=res[0].data).toMARCXML()).decode(db.encoding)
    else:
        search = ZClient()
        search.connect(db.host,
                       db.port,
                       db.db,
                       'RUSMARC',
                       db.encoding)
        book = search.get_book(kwargs['id'])
        if book:
            book = book[0]
    return render_to_response(kwargs['tpl'], locals())
