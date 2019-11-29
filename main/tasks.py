import logging

home_dir = 'log_folder/'

# Создаем регистратор логов
# Присваеваем ему имя и указываем минимальный уровень сообщений, на который он будет реагировать
logger = logging.Logger('rq_log', 'INFO')

# Создаем обработчик, который записывает логи на диск
# Указываем ему путь к файлу, в который он должен будет писать сообщения
file_handler = logging.FileHandler(home_dir + '/logs/rq_log')

# Указываем обработчику формат, в котором сообщения будут записываться в файл
# В файл будет записываться дата и время сообщения
file_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s", datefmt='%Y-%m-%d %H:%M:%S'))

# Указываем минимальный уровень сообщений, на которые будет реагировать данный обработчик
# В данном случае сообщения уровня DEBUG он будет отвергать
file_handler.setLevel(logging.INFO)

# Привязываем обработчик к регистратору
logger.addHandler(file_handler)


def rq_task():

    # Выводим в лог сообщения для тестирования работы регистратора
    logger.info('RQ_LOG Message')
