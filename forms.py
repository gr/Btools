# -*- coding: utf-8 -*-
from django import forms
from models import BookDB
from helper import QUERY_TYPE_CHOICE, SYNTAX_CHOICE

class QueryForm(forms.Form):
    db = forms.ModelChoiceField(
        queryset=BookDB.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={'class':'dbSelect'}), 
        error_messages={'required':'Select Database', 
                        'invalid_choice':'We know nothing about this Database'})
    query_type = forms.ChoiceField(choices=QUERY_TYPE_CHOICE, 
        error_messages={'required': 'Select Query Type', 
                        'invalid_choice': 'We know nothing about this Query Type'})
    syntax = forms.ChoiceField(choices=SYNTAX_CHOICE, 
        error_messages={'required':'Select Syntax', 
                        'max_length':'Max length is 250 symbols'})
    query = forms.CharField(max_length=250, widget=forms.widgets.Textarea(attrs={'rows':'10', 'cols':'62'}),
        error_messages={'required':'Can\'t be blank', 
                        'max_length':'Max length is 250 symbols'})
    charset_in = forms.CharField(max_length=50, 
        error_messages={'required':'utf-8, koi8, etc.', 
                        'max_length':'Max length is 250 symbols'})
    charset_out = forms.CharField(max_length=50, 
        error_messages={'required':'utf-8, koi8, etc.', 
                        'max_length':'Max length is 250 symbols'})
                        
                        
class SearchAjaxForm(forms.Form):
    db_url = forms.CharField(max_length=50)
    query_type = forms.CharField(max_length=10)
    query = forms.CharField(max_length=250)
    start = forms.IntegerField(min_value=0)
    lenght = forms.IntegerField(min_value=0, max_value=100)                   
