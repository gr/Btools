# -*- coding: utf-8 -*-
from django import forms
from models import BookDB
from choice import QUERY_TYPE_CHOICE, SYNTAX_CHOICE

class QueryForm(forms.Form):
    db = forms.ModelChoiceField(queryset=BookDB.objects.all(), empty_label=None, 
<<<<<<< HEAD
        error_messages={'required':'Select Database', 
                        'invalid_choice':'We know nothing about this Database'})
    query_type = forms.ChoiceField(choices=QUERY_TYPE_CHOICES, 
        error_messages={'required': 'Select Query Type', 
                        'invalid_choice': 'We know nothing about this Query Type'})
    syntax = forms.ChoiceField(choices=SYNTAX_CHOICES, 
        error_messages={'required':'Select Syntax', 
                        'max_length':'Max length is 250 symbols'})
    query = forms.CharField(max_length=250, widget=forms.widgets.Textarea(attrs={'rows':'10', 'cols':'62'}),
        error_messages={'required':'Can\'t be blank', 
                        'max_length':'Max length is 250 symbols'})
=======
        error_messages={'required':'Please, choise database', 
                        'invalid_choice':'Please, don\'t detroy our soft'})
    query_type = forms.ChoiceField(choices=QUERY_TYPE_CHOICE, 
        error_messages={'required': 'Please, query type', 
                        'invalid_choice': 'Please, don\'t detroy our soft'})
    query = forms.CharField(max_length=250, widget=forms.widgets.Textarea(attrs={'rows':'10', 'cols':'62'}),
        error_messages={'required':'Please, type the query', 
                        'max_length':'Sorry, max query lenght is 250 symbols'})
    syntax = forms.ChoiceField(choices=SYNTAX_CHOICE, 
        error_messages={'required':'Please, choice syntax', 
                        'max_length':'Sorry, max query lenght is 250 symbols'})
>>>>>>> origin/master
    charset = forms.CharField(max_length=250, 
        error_messages={'required':'utf-8, koi8, etc.', 
                        'max_length':'Max length is 250 symbols'})
