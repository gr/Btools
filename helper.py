# -*- coding: utf-8 -*-
"""
use in froms, models
"""
QUERY_TYPE_CHOICE = (('CCL', 'CCL'), 
                      ('S-CCL','S-CCL'), 
                      ('CQL','CQL'), 
                      ('S-CQL','S-CQL'), 
                      ('PQF','PQF'), 
                      ('C2','C2'), 
                      ('ZSQL','ZSQL'), 
                      ('CQL-TREE','CQL-TREE'))
"""
use in froms, models
"""                                            
SYNTAX_CHOICE = (('RUSMARC', 'RUSMARC'), 
                  ('USMARC', 'USMARC'), 
                  ('USMARCnonstrict', 'USMARCnonstrict'), 
                  ('UKMARC', 'UKMARC'), 
                  ('SUTRS', 'SUTRS'), 
                  ('XML', 'XML'),
                  ('SGML', 'SGML'),
                  ('GRS-1', 'GRS-1'),
                  ('OPAC', 'OPAC'),
                  ('EXPLAIN', 'EXPLAIN'))

"""
For extracting variables from Django template processor context
use in btags
"""
def is_var(dict, key):
    if dict.has_key(key):
        return dict[key]
    try:
        return int(key)
    except:
        if key[0] == key[-1] and key[0] in ['\'','"']:
            return key[1:-1]
        else:
            return key

"""
Get first or last N elements
"""
cut_array = lambda list, len: list[:int(len)] if int(len)>0 else list[int(len):]

"""
helper for book rendering
initialize in models
use in templates\btags\book.html
"""
class Output:
    def __init__(self, fields = None, encoding = ''):
        self.encoding = encoding
        self.fields = fields

    def __getattr__(self, name):
        field = name[1:].split('__')
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
