from django.core.exceptions import ValidationError
from profanity.extras import ProfanityFilter


words = []
with open('data/filter_profanity.txt', 'r', encoding='utf-8') as f:
    words = [line.strip() for line in f.readlines()]

pf = ProfanityFilter()
pf.append_words(words)


def validate_is_profane_russian(value):
    if pf.is_profane(value) is True:
        raise ValidationError('Некорректный вопрос')
