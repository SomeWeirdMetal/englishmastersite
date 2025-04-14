"""Модуль для работы со словарём терминов."""
import os
from django.conf import settings

VPATH = os.path.join(settings.BASE_DIR, 'data', 'vocabulary.csv')


def get_words():
    """Получает список слов из словаря.

    Returns:
        list: Список терминов в формате [номер, слово, определение]
    """
    words = []
    try:
        with open(VPATH, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file.readlines()[1:], start=1):
                word, definition = line.strip().split(";", maxsplit=1)
                words.append([line_num, word, definition])
    except FileNotFoundError:
        pass
    return words


def write_word(new_word, new_definition):
    """Добавляет новое слово в словарь.

    Args:
        new_word (str): Новый термин
        new_definition (str): Определение термина

    Raises:
        ValueError: Если файл словаря не найден
    """
    new_word_line = f"{new_word};{new_definition}\n"

    try:
        with open(VPATH, "r+", encoding="utf-8") as file:
            lines = [line.strip() for line in file]

            if not lines:
                raise ValueError("Файл словаря повреждён или пуст")

            title = lines[0]
            existing_words = lines[1:]
            updated_words = existing_words + [new_word_line.strip()]
            updated_words.sort()

            file.seek(0)
            file.write("\n".join([title] + updated_words))
            file.truncate()

    except FileNotFoundError as exc:
        raise ValueError("Файл словаря не найден") from exc


def get_words_stats():
    """Собирает статистику по словарю.

    Returns:
        dict: Словарь с метриками:
            - terms_all: Общее количество терминов
            - terms_own: Терминов из базы
            - terms_added: Терминов добавленных пользователем
            - words_avg: Средняя длина определения
            - words_max: Максимальная длина определения
            - words_min: Минимальная длина определения
    """
    stats = {
        "terms_all": 0,
        "terms_own": 0,
        "terms_added": 0,
        "words_avg": 0,
        "words_max": 0,
        "words_min": 0
    }
    defin_lengths = []

    try:
        with open(VPATH, "r", encoding="utf-8") as file:
            for line in file.readlines()[1:]:
                parts = line.strip().split(";")
                if len(parts) < 3:
                    continue

                _, definition, added_by = parts
                words = definition.split()
                defin_lengths.append(len(words))

                if "user" in added_by:
                    stats["terms_added"] += 1
                elif "db" in added_by:
                    stats["terms_own"] += 1

        if defin_lengths:
            stats.update({
                "terms_all": stats["terms_own"] + stats["terms_added"],
                "words_avg": round(sum(defin_lengths) / len(defin_lengths), 1),
                "words_max": max(defin_lengths),
                "words_min": min(defin_lengths)
            })

    except FileNotFoundError:
        pass

    return stats
