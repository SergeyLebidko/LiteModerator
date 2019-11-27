from django import template
from django.utils.html import mark_safe
from main.models import ForbiddenWord, PermittedWord
from re import sub

register = template.Library()

forbidden_list = ForbiddenWord.objects.all().values('word')
permitted_list = PermittedWord.objects.all().values('word')


def check_wrong_words(text):
    output_text = ''

    # Разбиваем исходный текст на отдельные элементы (для разбиения используется пробел)
    for word in text.split():

        # Из каждого элемента выделяем часть, которая состоит только из букв (т.е. отбрасываем знаки препинания)
        word_for_check = sub(r'[^\w]+', '', word)

        # Проверяем, нужно ли помечать слово, как матерное
        need_mark = False
        if check_word_for_forbidden(word_for_check, forbidden_list):
            need_mark = not check_word_for_permitted(word_for_check, permitted_list)

        # В зависимости от значения флага, помечаем или не помечаем слово
        # Знаки препинания в любом случае остаются не помеченнными
        if need_mark:
            t = word.partition(word_for_check)
            output_text += '<font color="red">'+t[1]+'</font>'+t[2]+' '
            continue

        output_text += word+' '

    # Возвращаем подготовленную строку
    return mark_safe(output_text.rstrip())


# Функция возвращает True, если слово содержит корень из перечня корней матерных слов
def check_word_for_forbidden(word, forbidden_list):
    for forbidden in forbidden_list:
        if forbidden['word'].lower() in word.lower():
            return True


# Функция возвращает True, если слово является словом исключением
def check_word_for_permitted(word, permitted_list):
    for permitted in permitted_list:
        if word.lower() == permitted['word'].lower():
            return True


# Регистрируем фильтр
register.filter('check_wrong_words', check_wrong_words)
