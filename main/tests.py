from django.test import TestCase
from re import findall, DOTALL

from .models import Review, Doctor, Specialty, ForbiddenWord, PermittedWord
from .templatetags.filters import check_wrong_words


test_texts_for_review_model = [
            ('Проверка неизменяемости нормального текста.', 'Проверка неизменяемости нормального текста.'),
            ('Проверка удаления повторяющихся знаков.....', 'Проверка удаления повторяющихся знаков.'),
            ('Проверка удаления пробелов перед знаками ?', 'Проверка удаления пробелов перед знаками?'),
            ('Проверка удаления      лишних пробелов', 'Проверка удаления лишних пробелов'),
            ('Проверка количества пробелов,     после знака', 'Проверка количества пробелов, после знака'),
            ('проверка ПОВЕДЕНИЯ при обнаружении более шести заглавных. ПРЕДЛОЖЕНИЯ должны быть КОРРЕКТНЫ.',
             'Проверка поведения при обнаружении более шести заглавных. Предложения должны быть корректны.')
        ]


test_texts_for_filter = [
    ('Предложение без мата', []),
    ('Сука, пиздец, на хуй', ['Сука', 'пиздец', 'хуй']),
    ('Предложение со словом оскорблять', [])
]


# Класс для тестирования формирования текста отзыва
class TestReviewModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        fictitious_specialty = Specialty(name='fictitious_specialty')
        fictitious_specialty.save()

        fictitious_doctor = Doctor(fio='fictitious_doctor')
        fictitious_doctor.save()
        fictitious_doctor.specialty.add(fictitious_specialty)

        for test_text in test_texts_for_review_model:
            Review.objects.create(
                doctor=fictitious_doctor,
                user=None,
                origin_text=test_text[0],
                moderation_flag=False,
                user_ip='127.0.0.1'
            )

    def test_finished_text_creation(self):
        for review in Review.objects.all():
            with self.subTest():
                self.assertEqual(review.create_text_for_moderator(), test_texts_for_review_model[review.pk-1][1])


# Класс для тестирования фильтра выделения матерных слов
class TestFilter(TestCase):

    @classmethod
    def setUpTestData(cls):
        forbidden = ['сук', 'еба', 'хуй', 'пизд', 'блять']
        permitted = ['оскорблять']
        for word in forbidden:
            ForbiddenWord.objects.create(word=word)
        for word in permitted:
            PermittedWord.objects.create(word=word)

    def test_filter(self):
        for text, wrong_words in test_texts_for_filter:
            with self.subTest():
                self.assertEqual(findall(r'<font color="red">(.*?)</font>', check_wrong_words(text)), wrong_words)

