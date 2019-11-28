from django.core.management.base import BaseCommand

import logging
import sys

home_dir = 'log_folder/'


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Создаем регистратор логов
        # Присваеваем ему имя и указываем минимальный уровень сообщений, на который он будет реагировать
        logger = logging.Logger('pult_mis_actions', 'DEBUG')

        # Создаем обработчик, который записывающий логи на диск
        # Указываем ему путь к файлу, в который он должен будет писать сообщения
        file_handler = logging.FileHandler(home_dir + '/logs/pult_mis_actions')

        # Указываем обработчику формат, в котором сообщения будут записываться в файл
        # В файл будет записываться дата и время сообщения
        file_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s", datefmt='%Y-%m-%d %H:%M:%S'))

        # Указываем минимальный уровень сообщений, на которые будет реагировать данный обработчик
        # В данном случае сообщения уровня DEBUG он будет отвергать
        file_handler.setLevel(logging.INFO)

        # Привязываем обработчик к регистратору
        logger.addHandler(file_handler)

        # Создаем еще один обработчик, который будет выводить файлы в поток
        # В данном случае - в стандартный поток вывода - консоль
        console_handler = logging.StreamHandler(sys.stdout)

        # Для этого обработчика указываем минимальный уровень логов, которые он будет выводить - DEBUG
        console_handler.setLevel(logging.DEBUG)

        # Привязываем обработчик к регистратору
        logger.addHandler(console_handler)

        # Выводим в лог сообщения для тестирования работы регистратора
        logger.info('Сообщение уровня INFO. Оно должно попасть и в консоль и в файл')
        logger.debug('Сообщение уровня DEBUG. Оно должно попасть только в консоль')
