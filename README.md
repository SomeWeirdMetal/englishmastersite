# englishmastersite
Веб-приложение для тренировки по английскому языку,
интерактивный тренажёр для изучения английского языка с:
- Упражнениями по грамматике
- Словарём терминов
- Системой отзывов
  
**Как стартовать**

1. Клонировать репозиторий
git clone https://github.com/SomeWeirdMetal/englishmastersite.git
cd englishmastersite
-или-
Скачать с github и разместить в папке с проектами

2. Настройка виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows

3. Установка требований
pip install -r requirements.txt

4. Запуск сервера
python manage.py runserver

Откройте в браузере при запущенном сервере:  
http://127.0.0.1:8000
