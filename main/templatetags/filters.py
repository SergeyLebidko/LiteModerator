from django import template
from main.models import ForbiddenWord, PermittedWords


register = template.Library()


def check_wrong_words(text):
    return text


register.filter('check_wrong_words', check_wrong_words)
