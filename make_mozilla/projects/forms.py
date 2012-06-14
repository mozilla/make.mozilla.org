from django import forms
from make_mozilla.projects.models import Topic, Difficulty, Skill
from make_mozilla.tools.models import Tool

class FilterForm(forms.Form):
    difficulty = forms.ModelChoiceField(
        required=False,
        queryset=Difficulty.objects.all(),
        empty_label='difficulty',
        to_field_name='value')
    topic = forms.ModelChoiceField(
        required=False,
        queryset=Topic.objects.all(),
        empty_label='topic',
        to_field_name='value')
    tool = forms.ModelChoiceField(
        required=False,
        queryset=Tool.objects.all(),
        empty_label='tool',
        to_field_name='slug')
    skill = forms.ModelChoiceField(
        required=False,
        queryset=Skill.objects.all(),
        empty_label='skill',
        to_field_name='value')
