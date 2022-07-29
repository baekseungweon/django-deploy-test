from django import forms
from players.models import Player


class PlayerForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = ['name', 'coin']
        widgets = {'name': forms.TextInput(attrs={
            'class':'name',
            'placeholder': '닉네임을 입력하세요.'}),
            'coin': forms.TextInput(attrs={
            'class':'coin',
            'placeholder': '코인 수량을 입력하세요.'
            })}
