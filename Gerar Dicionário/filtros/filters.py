# filters.py

def lowercase_letters(combination_str):
    return combination_str.strip().islower()

def uppercase_start(combination_str):
    return combination_str[0].isupper()

def start_number(combination_str):
    return combination_str[0].isdigit()

def final_number(combination_str):
    return combination_str[-2].isdigit()

def start_especiais(combination_str):
    return not combination_str[0].isalnum()

def final_especiais(combination_str):
    return not combination_str[-2].isalnum()

def select_filter(choice):
    if choice == 'Apenas caracteres maiúsculos no início':
        return uppercase_start
    elif choice == 'Apenas números no início':
        return start_number
    elif choice == 'Apenas números no final':
        return final_number
    elif choice == 'Apenas caracteres especiais no início':
        return start_especiais
    elif choice == 'Apenas caracteres especiais no final':
        return final_especiais
    else:
        return None
