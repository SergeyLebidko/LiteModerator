from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

from .models import Review


# Форма для регистрации нового пользователя
class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


# Форма для добавления нового отзыва
class ReviewForm(forms.ModelForm):
    origin_text = forms.CharField(widget=forms.widgets.Textarea(attrs={'cols': 120}))

    class Meta:
        model = Review
        fields = ['origin_text']

    def clean(self):
        super().clean()
        origin_text = self.cleaned_data['origin_text']
        if len(origin_text) < 100:
            errors = {'origin_text': ValidationError('Должно быть хотя бы 100 символов!')}
            raise ValidationError(errors)
