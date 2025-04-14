"""Модуль представлений"""
from django.shortcuts import render
from django.core.cache import cache
from . import feed_work
from . import grammar_work
from . import vocab_work

def index(request):
    """Отображает главную страницу сайта."""
    return render(request, "index.html")


def feedback(request):
    """
    Обрабатывает отправку отзывов и отображает страницу с формой.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        text = request.POST.get('text', '').strip()
        context = {"user": name}

        if len(name) == 0:
            context["success"] = False
            context["comment"] = "Имя не может быть пустым"
        elif len(text) == 0:
            context["success"] = False
            context["comment"] = "Отзыв не может быть пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваш отзыв принят!"
            feed_work.write_feed(name, text)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "feed_result.html", context)

    feedbacks = feed_work.read_feed()
    return render(request, 'feedback.html', {'feedbacks': feedbacks})


def grammar(request):
    """
    Обрабатывает грамматические упражнения и отображает результаты.
    """
    if request.method == 'POST':
        exercises = grammar_work.read_exerc()
        results = []
        correct = 0
        for ex in exercises:
            user_answer = request.POST.get(f'answer_{ex["id"]}', '').strip()
            is_correct = user_answer.lower() == ex["answer"].lower()
            if is_correct:
                correct += 1

            results.append({
                'id': ex["id"],
                'sentence': ex["sentence"],
                'answer': ex["answer"],
                'user_answer': user_answer,
                'is_correct': is_correct
            })

        total = len(exercises)
        score = int((correct / total) * 100) if total > 0 else 0
        return render(request, 'grammar_result.html', {
            'results': results,
            'correct': correct,
            'total': total,
            'score': score
        })

    exercises = grammar_work.read_exerc()
    return render(request, 'grammar.html', {'exercises': exercises})


def wordlist(request):
    """Отображает список слов словаря.

    Args:
        request: HttpRequest объект

    Returns:
        HttpResponse: Страница со словарем
    """
    words = vocab_work.get_words()
    return render(request, "vocabulary.html", context={"words": words})


def add_word(request):
    """Отображает форму добавления нового слова.

    Args:
        request: HttpRequest объект

    Returns:
        HttpResponse: Страница с формой добавления слова
    """
    return render(request, "add_word.html")


def send_word(request):
    """Обрабатывает отправку нового слова.

    Args:
        request: HttpRequest объект

    Returns:
        HttpResponse: Результат добавления слова или форма с ошибками
    """
    if request.method != "POST":
        return add_word(request)

    cache.clear()
    user_name = request.POST.get("name", "")
    new_word = request.POST.get("new_word", "").strip()
    new_definition = request.POST.get("new_definition", "").strip().replace(";", ",")

    context = {
        "user": user_name,
        "success": False,
        "comment": "",
        "success-title": ""
    }

    if not new_definition:
        context["comment"] = "Описание должно быть не пустым"
    elif not new_word:
        context["comment"] = "Термин должен быть не пустым"
    else:
        vocab_work.write_word(new_word, new_definition)
        context.update({
            "success": True,
            "comment": "Ваш термин принят"
        })

    return render(request, "word_request.html", context)


def show_stats(request):
    """Отображает статистику по словарю.

    Args:
        request: HttpRequest объект

    Returns:
        HttpResponse: Страница со статистикой
    """
    stats = vocab_work.get_words_stats()
    return render(request, "stats.html", stats)
