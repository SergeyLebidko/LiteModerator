from django.db import models
from django.contrib.auth.models import User


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
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='ФИО врача')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Пользователь, оставивший отзыв')

    dt_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания отзыва')
    dt_updated = models.DateTimeField(auto_now=True, verbose_name='Дата и время редактирования отзыва')
    origin_text = models.TextField(blank=False, verbose_name='Исходный отзыв')
    finished_text = models.TextField(blank=False, verbose_name='Обработанный отзыв')
    moderation_flag = models.BooleanField(default=False, null=False, verbose_name='Отзыв отмодерирован')

    user_ip = models.GenericIPAddressField(protocol='IPv4', verbose_name='ip-адрес пользователя')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-dt_created']


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
