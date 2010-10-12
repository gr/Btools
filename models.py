# -*- coding: utf-8 -*-
from django.db.models import *

class BookDB(Model):
    name = CharField(u'Название', max_length=50)
    host = CharField(u'Хост', max_length=50)
    port = IntegerField(u'Порт', default=210)
    db = CharField(u'База данных', max_length=50)
    encoding = CharField(u'Кодировка', max_length=50)
    url = CharField(u'url', max_length=50)
    about = TextField(u'Описание базы данных', blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u'База данных'
        verbose_name_plural = u'Базы данных'
