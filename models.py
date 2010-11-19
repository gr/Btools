# -*- coding: utf-8 -*-
from django.db.models import *
from choice import QUERY_TYPE_CHOICES, SYNTAX_CHOICES
from ZClient import ZClient, Output
import base64


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
        if value in ( False, None, '' ):
            return value
        else:
            pickling_books = [ x.fields for x in value ]
            return base64.encodestring(pickle.dumps(pickling_books, 2))
        
    def to_python(self, value):
        if not isinstance(value, basestring):
            return value 
        books_fields = pickle.loads(base64.decodestring(value))
        return [ Output( book_fields, 'utf-8') for book_fields in books_fields ]


class BookDB(Model):
    name = CharField(u'Название', max_length=50)
    host = CharField(u'Хост', max_length=50)
    port = IntegerField(u'Порт', default=210)
    db = CharField(u'База данных', max_length=50)
    syntax = CharField(u'Синтаксис', max_length=50, choices=SYNTAX_CHOICES)
    encoding = CharField(u'Кодировка', max_length=50)
    url = CharField(u'url', max_length=50)
    about = TextField(u'Описание базы данных', blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u'База данных'
        verbose_name_plural = u'Базы данных'
        
    def connect(self):
         handle = ZClient()
         handle.connect(self.host,
                        self.port,
                        self.db,
                        self.syntax,
                        self.encoding)
         return handle
   
        
class BookSet(Model):
    name = CharField(u'Название', max_length=50)
    db = ForeignKey(BookDB)
    query_type = CharField(u'Тип запроса', max_length=50, choices=QUERY_TYPE_CHOICES)
    query = TextField(u'Запрос', blank=True)
    time = TimeField(u'Обновляется каждый день, в')
    number_of_books = IntegerField(u'Количество книг', editable=False, null=True)
    last_time_update = DateTimeField(u'Последний раз обновлялось', editable=False, auto_now=True)
    view_me = BooleanField(u'Показывать на сайте', default=False)
    about = TextField(u'Описание набора книг, будет выводиться на сайте', blank=True)
    comment = TextField(u'Техническое описание набора книг, доступно только из админки', blank=True)
    books = BooksField(editable=False)
    
    def save(self):
        search = self.db.connect()
        self.books, self.number_of_books = search.query(query_type=self.query_type, query=self.query, length=1000)
        super(BookSet, self).save()    
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u'Набор книг'
        verbose_name_plural = u'Наборы книг'
