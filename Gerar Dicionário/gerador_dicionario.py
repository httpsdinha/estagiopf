import itertools
import os
import re

# Definindo os caracteres a serem usados
characters_numbers = "0123456789"
characters_uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
characters_lowercase = "abcdefghijklmnopqrstuvwxyz"
characters_especiais = "@#*_-"
characters_padrao = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*()_-+=?"
characters = input("Digite os caracteres a serem usados: ") or characters_padrao

# Definindo o tamanho dos dígitos e o tamanho máximo do arquivo
tamanho_digitos = (int(input("Digite o tamanho dos dígitos: ")))
max_file_size_mb = int(input("Digite o tamanho máximo do arquivo em MB: "))
max_file_size_kb = max_file_size_mb * 1024  # Convertendo MB para KB
max_file_size = max_file_size_kb * 1024  # Convertendo KB para bytes

#  Inicializando variáveis
file_index = 0
file_count = 1
current_file_name = f"arquivo_{file_index}.txt"
current_file = open(current_file_name, "w")
current_file_size = 0
first_combination = None  

def sanitize_filename(filename):
    # Remove caracteres inválidos para nomes de arquivos
    return re.sub(r'[<>:"/\|?*]', 'â', filename)

# Função para gerar combinações de caracteres
def generate_combinations(characters, length, filter_func=None):
    combinations = itertools.product(characters, repeat=length)
    for combination in combinations:
        combination_str = ''.join(combination) + "\n"
        if filter_func is None or filter_func(combination_str):
            yield combination_str

# Funções de filtro
def lowercase_letters(combination_str):
    return combination_str.strip().islower()

def uppercase_start (combination_str):
    return combination_str[0].isupper()

def start_number(combination_str):
    return combination_str[0].isdigit()

def final_number(combination_str):
    return combination_str[-2].isdigit()

def start_especiais(combination_str):
    return not combination_str[0].isalnum()

def final_especiais(combination_str):
    return not combination_str[-2].isalnum()


print("Escolha o modo de geração do dicionário:")
print("1. Apenas caracteres maiúsculos no início")
print("2. Apenas números no início")
print("3. Apenas números no final")
print("4. Apenas caracteres especiais no início")
print("5. Apenas caracteres especiais no final")
print("6. Nenhum filtro")
    
choice = input("Digite o número da opção desejada: ")   

# Define o filtro com base na escolha do usuário
if choice == '1':
    filter_func = uppercase_start
elif choice == '2':
    filter_func = start_number
elif choice == '3':
    filter_func = final_number
elif choice == '4':
    filter_func = start_especiais
elif choice == '5':
    filter_func = final_especiais
elif choice == '6':
    filter_func = lowercase_letters
elif choice == '7':
    filter_func = None
else:
    print("Opção inválida.")
    filter_func = None

# Gerar todas as combinações possíveis de X caracteres
for combination_str in generate_combinations(characters,tamanho_digitos, filter_func):
    combination_size = len(combination_str.encode('utf-8'))  # Tamanho da combinação em bytes
    
    if current_file_size == 0:
        first_combination = combination_str.strip()  # Armazena a primeira combinação

    if current_file_size + combination_size > max_file_size:
        # Renomeia o arquivo com base na primeira e última combinação
        current_file.close()
        last_combination = combination_str.strip()
        new_file_name = f"{first_combination}_{last_combination}.txt"
        new_file_name = sanitize_filename(new_file_name)
        os.rename(current_file_name, new_file_name)
        
        # Abre um novo arquivo
        file_index += 1
        current_file_name = f"arquivo_{file_index}.txt"
        current_file = open(current_file_name, "w")
        current_file_size = 0
        first_combination = combination_str.strip()  # Primeira combinação do novo arquivo
        file_count += 1

    # Escreve a combinação no arquivo atual
    current_file.write(combination_str)
    current_file_size += combination_size

# Renomeia o último arquivo com base na primeira e última combinação
current_file.close()
if current_file_size > 0:
    last_combination = combination_str.strip()
    new_file_name = f"{first_combination}_{last_combination}.txt"
    os.rename(current_file_name, new_file_name)

print(f"Combinações geradas e distribuídas entre {file_count} arquivos, renomeados com o primeiro e último dígito de cada.")
