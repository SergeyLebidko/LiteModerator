from django.test import TestCase

from .models import Review, Doctor, Specialty


test_texts = [
            ('Проверка неизменяемости нормального текста.', 'Проверка неизменяемости нормального текста.'),
            ('Проверка удаления повторяющихся знаков.....', 'Проверка удаления повторяющихся знаков.'),
            ('Проверка удаления пробелов перед знаками ?', 'Проверка удаления пробелов перед знаками?'),
            ('Проверка удаления      лишних пробелов', 'Проверка удаления лишних пробелов'),
            ('Проверка количества пробелов,     после знака', 'Проверка количества пробелов, после знака'),
            ('проверка ПОВЕДЕНИЯ при обнаружении более шести заглавных. ПРЕДЛОЖЕНИЯ должны быть КОРРЕКТНЫ.',
             'Проверка поведения при обнаружении более шести заглавных. Предложения должны быть корректны.')
        ]


class TestReviewModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        fictitious_specialty = Specialty(name='fictitious_specialty')
        fictitious_specialty.save()

        fictitious_doctor = Doctor(fio='fictitious_doctor')
        fictitious_doctor.save()
        fictitious_doctor.specialty.add(fictitious_specialty)

        for test_text in test_texts:
            Review.objects.create(
                doctor=fictitious_doctor,
                user=None,
                origin_text=test_text[0],
                moderation_flag=False,
                user_ip='127.0.0.1'
            )

    def test_finished_text_creation(self):
        for key in range(1, len(test_texts)+1):
            review = Review.objects.get(pk=key)
            self.assertEqual(review.create_text_for_moderator(), test_texts[key-1][1])
