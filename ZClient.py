# -*def coding: utf-8 -*-
from PyZ3950 import zoom, zmarc
import cPickle

def rub_list(books=[]):
    res=[]
    for book in books:
        if book.f675__a: res.append(('','udc',book.f675__a))
        elif book.f686: res.append(('','bbc',book.f686__a))
    return set(res)

class Output:
    encoding='koi8-r'
    fields=[]
    _null=1

    def constructor(self, fields, encoding):
        self.encoding = encoding
        self.fields = fields

    def __getattr__(self, name):
        name = name[1:] 
        field = name.split('__')
        try:
            if len(field) == 1:
                return self.fields.get(int(field[0]),'')[0]
            elif len(field) == 2:
                for f in self.fields[int(field[0])][0][2]:
                    if f[0] == field[1]:
                        return f[1].decode(self.encoding)
            elif len(field) == 3:
                field[2] = int(field[2])
                for f in self.fields[int(field[0])][0][2]:
                    if f[0] == field[1] and field[2] == 1:
                        return f[1].decode(self.encoding)
                    elif f[0] == field[1] and field[2] > 1:
                        field[2] -= 1
        except:
            return ''
        return ''

    def referat(self):
        res = u''
        if self.f200__e: res+=': '+self.f200__e
        if self.f200__e__2: res+=': '+self.f200__e__2
        if self.f200__f: res+=' / '+self.f200__f 
        if self.f210__a or self.f210__c or self.f210__d:
            res+='.&nbsp;&#8212; '
            if self.f210__a: res+=self.f210__a+': '
            if self.f210__c: res+=self.f210__c+', '
            if self.f210__d: res+=self.f210__d
        if self.f215__a or self.f215__c: 
            res+='.&nbsp;&#8212; '
            if self.f215__a: res+=self.f215__a
            if self.f215__c: res+=': '+self.f215__c
        if self.f320__a: res+='.&nbsp;&#8212; '+self.f320__a
        return res


    def store(self):
        res = []
        asd=0
        try:
            for a in self.fields[999]:
                for b in a:                     
                    for f in b: 
                        if f[0] == 'b':
                            for i in res:
                                if i[0] == f[1].decode(self.encoding):
                                    for gg in b:
                                        if gg[0] == 'v':
                                            i[1]+=int(gg[1])
                                    asd=1
                            if not asd:
                                if f[1].decode(self.encoding) != '':
                                    qaz = []
                                    qaz.append(f[1].decode(self.encoding))
                                    qaz.append(1)
                                    res.append(qaz)
                            asd=0
        except:
            pass
        return res 

    def author(self):
        if self.f700__a and self.f700__g: 
            return self.f700__a+'&nbsp;'+self.f700__g
        elif self.f700__a and self.f700__b:
            return self.f700__a+'&nbsp;'+self.f700__b
        elif self.f700__a:
            return self.f700__a
        else: 
            return ''

    def author_short(self):
        if self.f700__a and self.f700__b: 
            return self.f700__a+'&nbsp;'+self.f700__b
        elif self.f700__a and self.f700__g:
            return self.f700__a+'&nbsp;'+self.f700__g
        elif self.f700__a:
            return self.f700__a
        else: 
            return ''
            
    def header(self):
        if self.f461:
            res = u''
            if self.f461__a__2: res+=self.f461__a__2
            
            if self.f461__e__1: res+=': '+self.f461__e__1 
            if self.f461__e__2: res+=': '+self.f461__e__2
            
            if self.f461__f: res+=' / '+self.f461__f
            
            if self.f461__a__3: res+='&nbsp;&#8212; '+self.f461__a__3
            if self.f461__a__4: res+='&nbsp;&#8212; '+self.f461__a__4
            
            if self.f461__c: res+=': '+self.f461__c
            if self.f461__d: res+=', '+self.f461__d
            
            if self.f461__a__1: res+='.&nbsp;&#8212; '+self.f461__a__1
           
            return res   
        else:
            return ''

    def code(self):
        return self.f999__h+' '+self.f999__i
        
    def title(self):
        if self.f200__h or self.f461__v: 
            return self.f200__a+'. '+self.f200__h + self.f461__v
        else: 
            return self.f200__a

    def id(self):
        return self.f001

    def isbn(self):
        return self.f010__a

    def about(self):
        return self.f300__a

    def link(self):
        return self.f856__u

    def type(self):
        return self.fields['database']
        
    def db(self):
        return self.fields['database']

class ZClient:
    connection = 0
    response = []
    encoding = 'koi8-r'
    
    def connect(self, host, port, db_name, syntax, encoding):
        self.connection = 0
        self.connection = zoom.Connection (host, port, databaseName=db_name, preferredRecordSyntax=syntax)
        self.encoding = encoding

    def set_db(self, db_name):
        if self.connection <> 0:
            self.connection.databaseName=db_name 

    def set_syntax(self, syntax):
        if self.connection <> 0:
            self.connection.preferredRecordSyntax=syntax

    def query(self, query_type, query, start=0, length=10):
        res = []
        query = zoom.Query(query_type, query.encode(self.encoding))
        self.response = self.connection.search(query)
        if len(self.response) < start: 
            start=0
        if len(self.response) < start+length:
            length = len(self.response)   
        for i in xrange(start, start+length):
            record = zmarc.MARC(MARC=self.response[i].data)
            p_record = Output()
            if self.connection.databaseName[-1:] == 's':
                record.fields['database'] = self.connection.databaseName[:-1]
            else:
                record.fields['database'] = self.connection.databaseName
#            record.fields['database'] = self.connection.databaseName[:-1]
            p_record.constructor(record.fields, self.encoding)
            res.append(p_record)
        return res, len(self.response)

    def get_book(self, book_id):
        query = '@attr 1=12 "'+str(int(book_id))+'"'
        return self.query('pqf',query)[0]

    def get_books(self, keyword, start=0, length=10):
        query = '@or @attr 1=7 "'+keyword+'"@attr 3=3 @attr 1=1035 "'+keyword+'"'
        return self.query('pqf',query, start, length)

    def serialize(self, file_name, books):
        fo = open(file_name, "wb")
        books.reverse()
        try:
            for book in books:
                if book.f010__a and book.f999__b != u'Худ фонд':
                    cPickle.dump(book.fields, fo)
            fo.close()
        except:
            return 0
        return 1
        
    def unserialize(self, file_name):
        last_books = []
        fo = open(file_name, "rb")
        try:
            while 1:
                p_record = Output()
                p_record.constructor(cPickle.load(fo), self.encoding)
                last_books.append(p_record)
        except:
            pass
        fo.close()
        return last_books
