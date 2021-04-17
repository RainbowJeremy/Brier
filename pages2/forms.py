from django import forms
import datetime
from .models import Estimate, Question, Forum


class ForumForm(forms.ModelForm):
    class Meta:
        model= Forum
        fields = ['topic', 'description', 'image']



class EstimateForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Explain your reasoning here',
                                                        'class': 'form-body',
                                                        'style' : 'height: 12em; width: 20rem; resize:none;',}),
                                                        required=False)

    estimate = forms.CharField(widget=forms.NumberInput(attrs={ 'class' : 'form-est-field',
                                                                "style":"width: 4.2em; height: 4em;", #" font-size: 1rem;",
                                                                }))

    class Meta:
        model = Estimate
        fields = ['estimate', 'body']
        labels = {'estimate':'prediction', 'body':''}

    def __init__(self, name= 'EstimateForm', *args, **kwargs): # this may be needed later to fix smtn, use Super().__init__(*args,**kwargs)
        self.__name__ = name
        super().__init__(*args, **kwargs)


class QuestionForm(forms.ModelForm):
    question = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'What are the chances...',
                                                        'class': "form-control rounded",
                                                        })) #.Textarea(attrs-{'rows':3}))

    class Meta:
        model = Question
        fields = ['question']
