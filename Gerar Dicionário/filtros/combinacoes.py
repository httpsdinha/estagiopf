import itertools

def generate_combinations(characters, length, filter_func=None):
    """
    Gera combinações de caracteres com o comprimento especificado.
    Aplica um filtro opcional às combinações.
    """
    combinations = itertools.product(characters, repeat=length)
    for combination in combinations:
        combination_str = ''.join(combination) + "\n"
        if filter_func is None or filter_func(combination_str):
            yield combination_str
