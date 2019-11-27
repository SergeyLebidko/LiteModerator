from django import template
from django.utils.html import mark_safe
from main.models import ForbiddenWord, PermittedWord
from re import sub

register = template.Library()


def check_wrong_words(text):
    forbidden_words = ForbiddenWord.objects.all()
    permitted_words = PermittedWord.objects.all()

    output_text = ''

    for word in text.split():
        word_for_check = sub(r'[^\w]+', '', word)

        # Если флаг ниже равен True, то предполагаем, что слово помечать не нужно
        need_mark = False
        for forbidden_word in forbidden_words:
            if word_for_check.lower().find(str(forbidden_word).lower()) != (-1):
                need_mark = True
                break

        # Если слово было помечено, как матерное, то надо проверить, не является ли оно словом-исключением
        if need_mark:
            for permitted_word in permitted_words:
                if word_for_check.lower() == str(permitted_word).lower():
                    need_mark = False
                    break

        # В зависимости от значения флага, помечаем или не помечаем слово
        # Знаки препинания в любом случае остаются не помеченнными
        if need_mark:
            t = word.partition(word_for_check)
            output_text += t[0]+'<font color="red">'+t[1]+'</font>'+t[2]+' '
            continue

        output_text += word+' '

    # Удаляем лишний конечный пробел
    output_text = output_text.rstrip()

    return mark_safe(output_text)


# Регистрируем фильтр
register.filter('check_wrong_words', check_wrong_words)
