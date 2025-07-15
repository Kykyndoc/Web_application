import re
from django import template

register = template.Library()

censor_list = ['Олимпиада', 'Лучшим', 'Наша', 'футбольных', '22']

@register.filter()
def censor(value):
    def replace_word(match):
        if not isinstance(value, str):
            raise TypeError("Фильтр 'censor' должен применяться только к строковым значениям!")
        word = match.group(0)  # Получаем найденное слово
        return word[0] + '*' * (len(word) - 1)  # Сохраняем первую букву и заменяем остальные на звездочки

    for word in censor_list:
        # Создаем регулярное выражение для поиска целого слова
        pattern = r'\b' + re.escape(word) + r'\b'
        # Заменяем целое слово, используя функцию обратного вызова
        value = re.sub(pattern, replace_word, value, flags=re.IGNORECASE)

    return value