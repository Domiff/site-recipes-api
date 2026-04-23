import re


def to_snake_case(name: str) -> str:
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def pluralize_word(word: str) -> str:
    if word.endswith("y") and len(word) > 1 and word[-2] not in "aeiou":
        return word[:-1] + "ies"
    if word.endswith(("s", "x", "z", "ch", "sh")):
        return word + "es"
    return word + "s"


def to_snake_plural(table_name) -> str:
    snake = to_snake_case(table_name)
    parts = snake.split("_")
    parts[-1] = pluralize_word(parts[-1])
    return "_".join(parts)
