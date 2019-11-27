from django.db import models
from django.contrib.auth.models import User
from re import sub, findall

# Регулярные выражения для замен символов
replace_templates = [
    # Блок регулярных выражений для замены идущих подряд знаков препинания
    (r'!+', '!'),
    (r'\?+', '?'),
    (r'\.+', '.'),
    (r',+', ','),
    (r':+', ':'),
    (r';+', ';'),
    (r'-+', '-'),

    # Блок регулярных выражений, удаляющих пробелы перед знаками препинания
    (r'\s+!', '!'),
    (r'\s+\?', '?'),
    (r'\s+\.', '.'),
    (r'\s+,', ','),
    (r'\s+:', ':'),
    (r'\s+;', ';'),
    (r'\s+-', '-')
]


# Модель для хранения специальностей
class Specialty(models.Model):
    name = models.CharField(max_length=100, verbose_name='Специальность')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


# Модель для хранения врачей
class Doctor(models.Model):
    fio = models.CharField(max_length=250, verbose_name='ФИО врача')
    specialty = models.ManyToManyField(Specialty, verbose_name='Специальность врача')

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'ФИО врача'
        verbose_name_plural = 'ФИО врачей'


# Модель для хранения отзывов
class Review(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='ФИО врача', db_index=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT,
                             verbose_name='Пользователь, оставивший отзыв', db_index=True)

    dt_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания отзыва')
    dt_updated = models.DateTimeField(auto_now=True, verbose_name='Дата и время редактирования отзыва')
    origin_text = models.TextField(blank=False, verbose_name='Исходный отзыв')
    finished_text = models.TextField(blank=False, verbose_name='Обработанный отзыв')
    moderation_flag = models.BooleanField(default=False, null=False, verbose_name='Отзыв отмодерирован')

    user_ip = models.GenericIPAddressField(protocol='IPv4', verbose_name='ip-адрес пользователя')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['dt_created']

    def create_text_for_moderator(self):
        # Готовим текст, который будет править модератор
        review_text = self.origin_text

        # Последовательно применяем к исходному тексту регулярные выражения для упорядочивания знаков препинания
        for regex, replacement_text in replace_templates:
            review_text = sub(regex, replacement_text, review_text)

        # Временная переменная, которая понадобиться для хранения исправляемого текста
        tmp_text = ''

        # После каждого знака препинания вставляем пробел
        for p in review_text:
            tmp_text += p
            if p in '.,-?!':
                tmp_text += ' '
        review_text = tmp_text

        # Удалаем лишние пробелы внутри текста (если они есть)
        review_text = sub(r'[\s]+', ' ', review_text)

        # Удаляем начальные и конечные пробелы (если они есть)
        review_text = review_text.strip()

        # Проверяем повторение шести или более заглавных символов и если нашли их, то исправляем текст
        if findall(r'[А-Я]{6,}', review_text):
            tmp_text = ''

            # Переменная, которая будет хранить отдельные предложения
            partition = ''

            for p in review_text:
                partition += p
                if p in '.!?':
                    if partition.startswith(' '):
                        tmp_text += ' ' + partition.strip().capitalize()
                    else:
                        tmp_text += partition.strip().capitalize()
                    partition = ''

            review_text = tmp_text

        return review_text


# Модель для хранения запрещенных слов
class ForbiddenWord(models.Model):
    word = models.CharField(max_length=100, verbose_name='Запрещенное слово')

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = 'Запрещенное слово'
        verbose_name_plural = 'Запрещенные слова'


# Модель для хранения слов-исключений
class PermittedWords(models.Model):
    word = models.CharField(max_length=100, verbose_name='Слово-исключение')

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = 'Слово-исключение'
        verbose_name_plural = 'Слова-исключения'
