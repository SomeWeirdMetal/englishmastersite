"""Модуль для работы с грамматическими упражнениями."""
import os
import csv
from django.conf import settings

GPATH = os.path.join(settings.BASE_DIR, 'data', 'grammar.csv')


def read_exerc():
    """
    Читает упражнения из CSV-файла.

    Returns:
        list: Список словарей с упражнениями, где каждый словарь содержит:
            - id (str): номер задания
            - sentence (str): предложение с пропуском
            - answer (str): правильный ответ
    """
    exercises = []
    try:
        with open(GPATH, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if len(row) == 3:
                    exercises.append({
                        'id': row[0],
                        'sentence': row[1],
                        'answer': row[2].strip()
                    })
    except FileNotFoundError:
        pass
    return exercises
