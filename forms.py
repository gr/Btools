# -*- coding: utf-8 -*-
from django import forms
from models import BookDB

class QueryForm(forms.Form):
    db = forms.ModelChoiceField(queryset=BookDB.objects.all(), empty_label=None, 
        error_messages={'required':'Please, choise database', 
                        'invalid_choice':'Please, don\'t detroy our soft'})
    query_type = forms.ChoiceField(choices=(('CCL', 'CCL'), 
                                            ('S-CCL','S-CCL'), 
                                            ('CQL','CQL'), 
                                            ('S-CQL','S-CQL'), 
                                            ('PQF','PQF'), 
                                            ('C2','C2'), 
                                            ('ZSQL','ZSQL'), 
                                            ('CQL-TREE','CQL-TREE')), 
        error_messages={'required': 'Please, query type', 
                        'invalid_choice': 'Please, don\'t detroy our soft'})
    query = forms.CharField(max_length=250, widget=forms.widgets.Textarea(attrs={'rows':'10', 'cols':'62'}),
        error_messages={'required':'Please, type the query', 
                        'max_length':'Sorry, max query lenght is 250 symbols'})
    syntax = forms.ChoiceField(choices=(('RUSMARC', 'RUSMARC'), 
                                        ('USMARC', 'USMARC'), 
                                        ('USMARCnonstrict', 'USMARCnonstrict'), 
                                        ('UKMARC', 'UKMARC'), 
                                        ('SUTRS', 'SUTRS'), 
                                        ('XML', 'XML'),
                                        ('SGML', 'SGML'),
                                        ('GRS-1', 'GRS-1'),
                                        ('OPAC', 'OPAC'),
                                        ('EXPLAIN', 'EXPLAIN')), 
        error_messages={'required':'Please, choice syntax', 
                        'max_length':'Sorry, max query lenght is 250 symbols'})
    charset = forms.CharField(max_length=250, 
        error_messages={'required':'Please, type the charset', 
                        'max_length':'Sorry, max query lenght is 250 symbols'})
