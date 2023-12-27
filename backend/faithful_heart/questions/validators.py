import os

from django.core.exceptions import ValidationError
from profanity.extras import ProfanityFilter

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_dir, "data", "filter_profanity.txt")

words = []
with open(file_path, "r", encoding="utf-8") as f:
    words = [line.strip() for line in f.readlines()]

pf = ProfanityFilter()
pf.append_words(words)


def validate_is_profane_russian(value):
    if pf.is_profane(value) is True:
        raise ValidationError("Некорректный вопрос")
