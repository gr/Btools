# -*- coding: utf-8 -*-
from django.db.models import *
from ZClient.ZClient import ZClient, Output
from django.conf import settings
from Typograf.typo import typografy

try:
    import cPickle as pickle
except ImportError:
    import pickle

class BookSet(Model):
    name = CharField(u'Название', max_length=50)
    QUERY_CHOICES = (
        ('CQL', 'CQL'),
        ('PQF', 'PQF'),
        ('CCL', 'CCL'),
    )
    DB_CHOICES = (
        ('books', 'books'),
        ('ebooks', 'ebooks'),
    )
    db = query_type = CharField(u'База данных', max_length=6, choices=DB_CHOICES)
    query_type = CharField(u'Тип запроса', max_length=3, choices=QUERY_CHOICES)
    query = TextField(u'Запрос', blank=True)
    time = TimeField(u'Обновляется каждый день, в')
    pickled_books = TextField(editable=False)
    number_of_books = IntegerField(u'Количество книг', editable=False, null=True)
    last_time_update = DateTimeField(u'Последний раз обновлялось', editable=False, auto_now=True)
    view_me = BooleanField(u'Показывать на сайте', default=False)
    about = TextField(u'Описание набора книг, будет выводиться на сайте', blank=True)
    typograf_about = TextField(default='none', editable=False)
    comment = TextField(u'Техническое описание набора книг, доступно только из админки', blank=True)
    
    def __getattr__(self, item):
        if item != 'books': 
            try:
                return self.__getitem__(item)
            except KeyError:
                raise AttributeError(item)
        else:
            books = []
            unpickled_books = pickle.loads(self.pickled_books.encode(settings.Z3950_CHARSET))
            for book in unpickled_books:
                p_record = Output()
                p_record.constructor(book, settings.Z3950_CHARSET)
                books.append(p_record)
            return books
        
    def __setattr__(self, item, value):
        if item != 'books':
            if not self.__dict__.has_key('_attrExample__initialised'):  # this test allows attributes to be set in the __init__ method
                return dict.__setattr__(self, item, value)
            elif self.__dict__.has_key(item):       # any normal attributes are handled normally
                dict.__setattr__(self, item, value)
            else:
                self.__setitem__(item, value)
        else:
            pickling_books = []
            value_len = len(value)
            for book in value:
                pickling_books.append(book.fields)
            self.pickled_books = pickle.dumps(pickling_books, 2).decode(settings.Z3950_CHARSET)
    
    def check_me(self):
         search = ZClient()
         search.connect(settings.Z3950_HOST,
                        settings.Z3950_PORT,
                        self.db,
                        settings.Z3950_SYNTAX,
                        settings.Z3950_CHARSET)
         self.books, self.number_of_books = search.query(query_type=self.query_type, query=self.query, length=1000)


    def save(self):
        self.check_me()
        if settings.TYPOGRAFY:
            typograf_about = typografy(self.about)
        else:
            typograf_about = self.about
        super(BookSet, self).save()    
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u'Набор книг'
        verbose_name_plural = u'Наборы книг'
    
