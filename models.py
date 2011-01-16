# -*- coding: utf-8 -*-
from django.db.models import *
from django.conf import settings
from helper import cut_array, Output, QUERY_TYPE_CHOICE, SYNTAX_CHOICE
from PyZ3950 import zoom, zmarc
from os import system
import base64, codecs


try:
    import cPickle as pickle
except ImportError:
    import pickle


class BooksField(TextField):
    """
        Field for easy save booksets in DB
    """
    __metaclass__ = SubfieldBase
    
    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        return self.get_prep_value(value)
    
    def value_to_string(self, model_instance):
        value = getattr(model_instance, self.attname, None)
        return self.get_prep_value(value)

    def get_prep_value(self, value):
        if value in ( False, None, '' ) or not isinstance(value, list):
            return value
        else:
            pickling_books = [ (x.fields, x.encoding) for x in value ]
            return base64.encodestring(pickle.dumps(pickling_books, 2))
        
    def to_python(self, value):
        if not isinstance(value, basestring) or value in ( False, None, '' ):
            return value 
        books_fields = pickle.loads(base64.decodestring(value))
        return [ Output( book_fields, encoding) for (book_fields, encoding) in books_fields ]


class BookDB(Model):
    name = CharField(u'Название', max_length=50)
    host = CharField(u'Хост', max_length=50)
    port = IntegerField(u'Порт', default=210)
    db = CharField(u'База данных', max_length=50)
    syntax = CharField(u'Синтаксис', max_length=50, choices=SYNTAX_CHOICE)
    encoding_in = CharField(u'Кодировка запроса', max_length=50)
    encoding_out = CharField(u'Кодировка ответа', max_length=50)
    url = CharField(u'url', max_length=50)
    about = TextField(u'Описание базы данных', blank=True)
    #id_prefix = TextField(u'id префикс', editable=False, null=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u'База данных'
        verbose_name_plural = u'Базы данных'

    def save(self, *args, **kw):
        book = self.query('PQF', '@attr 1=12 @attr 4=107 @attr 2=1 1000')[1]
        id_prefix = '\\'.join(book.f001.split('\\')[:-1])
        raise ERROR 
        super(BookSet, self).save(*args, **kw)
        
    """
    Return Z39.50 connection handle
    """        
    def connect(self):
         handle = zoom.Connection (host = self.host,
                                   port = self.port,
                                   databaseName = self.db,
                                   preferredRecordSyntax = self.syntax)
         return handle
    
    """
    Return array of books
    or 'Connection error: DB is not reachable' message
    book is Output class 
    """     
    def query(self, query_type, query):
        try:
            result = []
            connection = self.connect()
            query = zoom.Query(query_type, query.encode(self.encoding_in))
            response = connection.search(query)
            i = 0
            for raw_record in response:
                i += 1
                asd = raw_record.data
                record = zmarc.MARC(MARC=raw_record.data, strict = 0)
                result.append(Output(record.fields, self.encoding_out))
        except zoom.ConnectionError:
            result = 'Connection error: DB is not reachable'
        return result

    """
    Return book by id or 'Connection error: DB is not reachable' message
    book is Output class
    """
    def get_book(self, book_id):
        res = self.query('PQF', '@attr 1=12 "%s"' % book_id)
        if isinstance(res, basestring) or len(res) == 0:
            return res
        else:
            return res[0]


class BookSet(Model):
    name = CharField(u'Название', max_length=50)
    db = ForeignKey(BookDB)
    query_type = CharField(u'Тип запроса', max_length=50, choices=QUERY_TYPE_CHOICE)
    query = TextField(u'Запрос', blank=True)
    time = TimeField(u'Обновляется каждый день, в')
    number_of_books = IntegerField(u'Количество книг', editable=False, null=True)
    max_books = IntegerField(u'Максимальное количество книг в наборе', default=1000)
    last_time_update = DateTimeField(u'Последний раз обновлялось', editable=False, auto_now=True)
    view_me = BooleanField(u'Показывать на сайте', default=False)
    about = TextField(u'Описание набора книг, будет выводиться на сайте', blank=True)
    comment = TextField(u'Техническое описание набора книг, доступно только из админки', blank=True)
    books = BooksField(editable=False, null=True)
    
    def save(self, *args, **kw):
        # crontab not support seconds
        self.time = self.time.replace(self.time.hour, self.time.minute, 0)
        # update bset on save
        self.bookset_update(*args, **kw)
        # make crontab
        crontab = u'\n'.join(['%s %s * * * python %smanage.py bookset update \'%s\'' % (bset.time.minute, bset.time.hour, settings.PROJECT_ROOT, bset.name) for bset in BookSet.objects.all()])
        # crontab need end with null line
        codecs.open(settings.PROJECT_ROOT + 'crontab', 'w', 'utf-8').write(crontab+'\n')
        # load crontab
        system('crontab %scrontab' % settings.PROJECT_ROOT)

    def bookset_update(self, *args, **kw):
        books = self.db.query(query_type=self.query_type, query=self.query)
        if not isinstance(books, basestring):
            self.books = cut_array(books, self.max_books)
            self.number_of_books = len(self.books)
            super(BookSet, self).save(*args, **kw)
        
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u'Набор книг'
        verbose_name_plural = u'Наборы книг'
