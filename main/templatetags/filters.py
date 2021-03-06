from django import template
from django.utils.html import mark_safe
from main.models import ForbiddenWord, PermittedWord
from re import sub

register = template.Library()

forbidden_list = ForbiddenWord.objects.values_list('word', flat=True)
permitted_list = PermittedWord.objects.values_list('word', flat=True)


def check_wrong_words(text):
    output_text = ''

    # Разбиваем исходный текст на отдельные элементы (для разбиения используется пробел)
    for word in text.split():

        # Из каждого элемента выделяем часть, которая состоит только из букв (т.е. отбрасываем знаки препинания)
        word_for_check = sub(r'[^\w]+', '', word)

        # Проверяем, нужно ли помечать слово, как матерное
        need_mark = check_word_for_forbidden(word_for_check) and not check_word_for_permitted(word_for_check)

        # В зависимости от значения флага, помечаем или не помечаем слово
        # Знаки препинания в любом случае остаются не помеченнными
        if need_mark:
            partitions = word.partition(word_for_check)
            output_text += '<font color="red">'+partitions[1]+'</font>'+partitions[2]+' '
            continue

        output_text += word+' '

    # Возвращаем подготовленную строку
    return mark_safe(output_text.rstrip())


# Функция возвращает True, если слово содержит корень из перечня корней матерных слов
def check_word_for_forbidden(word):
    for forbidden in forbidden_list:
        if forbidden.lower() in word.lower():
            return True


# Функция возвращает True, если слово является словом исключением
def check_word_for_permitted(word):
    for permitted in permitted_list:
        if word.lower() == permitted.lower():
            return True


# Регистрируем фильтр
register.filter('check_wrong_words', check_wrong_words)
