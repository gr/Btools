# -*- coding: utf-8 -*-
from django.test import TestCase
from django.conf import settings
from models import BookDB, BookSet
from datetime import time
import subprocess


class Ttags(TestCase):
    def test_book_render(self):
        index = self.client.get('/debug/tpl/book_render.html')
        self.assertContains(index, 'index-card')
    
    def test_bookset_render(self):
        index = self.client.get('/debug/tpl/bookset_render.html')
        self.assertContains(index, 'BookSet render')

    def test_bookset_list_render(self):
        index = self.client.get('/debug/tpl/bookset_list_render.html')
        self.assertContains(index, 'BookSet List')
        
    def test_search_tag(self):
        index = self.client.get('/debug/tpl/search_tag.html')
        self.assertContains(index, 'Search tag')

  
class Db_crud(TestCase):
    def test_create(self, test_name='first_test'):
        result = BookDB.objects.create(name=test_name,
                                       host='62.76.8.149',
                                       port=210,
                                       db='avtref',
                                       syntax='RUSMARC',
                                       encoding_in='utf-8',
                                       encoding_out='utf-8',
                                       url='test_'+test_name,
                                       about='something about '+test_name)
        
        self.assertEqual(result.__unicode__(), result.name)
        self.assertEqual(result.name, test_name)
        return result

    def test_read(self):
        rec = self.test_create('second_test')
        rec.save()
        find = BookDB.objects.get(name='second_test')
        self.assertEqual(find.name, 'second_test')
        self.assertEqual(find.host, '62.76.8.149')
        self.assertEqual(find.port, 210)
        self.assertEqual(find.db, 'avtref')
        self.assertEqual(find.syntax, 'RUSMARC')
        self.assertEqual(find.encoding_in, 'utf-8')
        self.assertEqual(find.encoding_out, 'utf-8')
        self.assertEqual(find.url, 'test_second_test')
        self.assertEqual(find.about, 'something about second_test')
        self.assertNotEquals(find.connect(), None)
    
    def test_update(self):
        rec = self.test_create('third_test')
        rec.save()
        find = BookDB.objects.get(name='third_test')
        find.name = 'change_' + find.name
        find.host = 'change_' + find.host
        find.port = 666
        find.db = 'change_' + find.db
        find.syntax = 'change_' + find.syntax
        find.encoding_in = 'change_' + find.encoding_in
        find.encoding_out = 'change_' + find.encoding_out
        find.url = 'change_' + find.url
        find.about = 'change_' + find.about
        find.save()
        second = BookDB.objects.get(name='change_third_test')
        self.assertEqual(second.name, 'change_third_test')
        self.assertEqual(second.host, 'change_62.76.8.149')
        self.assertEqual(second.port, 666)
        self.assertEqual(second.db, 'change_avtref')
        self.assertEqual(second.syntax, 'change_RUSMARC')
        self.assertEqual(second.encoding_in, 'change_utf-8')
        self.assertEqual(second.encoding_out, 'change_utf-8')
        self.assertEqual(second.url, 'change_test_third_test')
        self.assertEqual(second.about, 'change_something about third_test')
        
    def test_delete(self):
        rec = self.test_create('fourth_test')
        rec.save()
        find = BookDB.objects.get(name='fourth_test')
        find.delete()


class BookSet_crud(TestCase):
    def test_create(self, test_name=u'first_test'):
        result = BookSet.objects.create(name=test_name,
                                        db=BookDB.objects.get(url='bgu'),
                                        query_type=u'CCL',
                                        query=u'"ток"',
                                        time=time(),
                                        max_books=1000,
                                        view_me=True,
                                        about=u'Something about '+test_name,
                                        comment=u'Tech comment about '+test_name)

        self.assertEqual(result.__unicode__(), result.name)
        self.assertEqual(result.name, test_name)
        return result                               

    def test_read(self):
        rec = self.test_create(u'second_test')
        rec.save()
        find = BookSet.objects.get(name=u'second_test')
        self.assertEqual(find.name, u'second_test')
        self.assertEqual(find.db.url, 'bgu')
        self.assertEqual(find.query_type, u'CCL')
        self.assertEqual(find.query, u'"ток"')
        self.assertEqual(find.max_books, 1000)
        self.assertEqual(find.view_me, True)
        self.assertEqual(find.about, u'Something about second_test')
        self.assertEqual(find.comment, u'Tech comment about second_test')
        self.assertEqual(find.number_of_books, 4)
        
    def test_update(self):
        rec = self.test_create('third_test')
        rec.save()
        find = BookSet.objects.get(name='third_test')
        find.name = 'third'
        find.query = u'"Иванов"' 
        find.max_books = 200.
        find.view_me = False
        find.about = 'about' 
        find.comment = 'comment'
        find.save()
        second = BookSet.objects.get(name='third')
        self.assertEqual(second.name, u'third')
        self.assertEqual(second.query_type, u'CCL')
        self.assertEqual(second.query, u'"Иванов"')
        self.assertEqual(second.max_books, 200)
        self.assertEqual(second.view_me, False)
        self.assertEqual(second.about, 'about')
        self.assertEqual(second.comment, 'comment')
        self.assertEqual(second.number_of_books, 57)
        self.assertEqual(second.db.url, 'bgu')
        
    def test_delete(self):
        rec = self.test_create('second_test')
        rec.save()
        find = BookSet.objects.get(name='second_test')
        find.delete()


class Managment(TestCase):
    def update_call(self, bookset_name):
        p = subprocess.Popen('python %smanage.py bookset update %s' % (settings.PROJECT_ROOT, bookset_name), shell=True, stdin=subprocess.PIPE, \
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
        return p.stdout.read()
        
    def test_bookset_update(self):
        self.assertEqual(self.update_call('\'ток\''), 'Successfully updates bookset "ток"\n')

    def test_bookset_update_nothing(self):
        self.assertEqual(self.update_call(''), 'Error: Set bookset which need to update\n')
    
    def test_bookset_update_not_created(self):
        self.assertEqual(self.update_call('\'йо-хо-хо\''), 'Error: BookSet "йо-хо-хо" does not exist\n')
        
        
class Fixtures(TestCase):
    def manage_call(self, params):
        p = subprocess.Popen('python %smanage.py %s' % (settings.PROJECT_ROOT, params), shell=True, stdin=subprocess.PIPE, \
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
        return p.stdout.read()
        
    def test_db_dump(self):
        result = self.manage_call('dumpdata btools.BookDB')
        return result
        
    def test_db_load(self):
        rec = self.test_db_dump()
        
    def test_bset_dump(self):
        result = self.manage_call('dumpdata btools.BookSet')
        return result
        
    def test_bset_load(self):
        rec = self.test_bset_dump()
