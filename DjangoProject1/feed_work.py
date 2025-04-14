"""Модуль для работы с отзывами пользователей."""
import os
import csv
from datetime import datetime
from django.conf import settings


FPATH = os.path.join(settings.BASE_DIR, 'data', 'feedback.csv')


def write_feed(name, text):
    """
    Записывает новый отзыв в файл.

    Args:
        name (str): Имя пользователя
        text (str): Текст отзыва
    """
    if name and text:
        with open(FPATH, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([
                datetime.now().isoformat(),
                name,
                text
            ])


def read_feed():
    """
    Читает все отзывы из файла.

    Returns:
        list: Список отзывов, отсортированных по дате (новые сначала),
              где каждый отзыв представлен словарем с ключами:
              - date (str): дата отзыва
              - name (str): имя пользователя
              - text (str): текст отзыва
    """
    feedbacks = []
    try:
        with open(FPATH, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if len(row) == 3:
                    feedbacks.append({
                        'date': row[0],
                        'name': row[1],
                        'text': row[2]
                    })
            return sorted(feedbacks, key=lambda x: x['date'], reverse=True)
    except (FileNotFoundError, StopIteration):
        return []
