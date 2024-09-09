import itertools
import os
import re

#characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:'\",.<>?/"
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*()_-+=?"
tamanho_digitos = (int(input("Digite o tamanho dos dígitos: ")))
max_file_size_mb = int(input("Digite o tamanho máximo do arquivo em MB: "))
max_file_size_kb = max_file_size_mb * 1024  # Convertendo MB para KB
max_file_size = max_file_size_kb * 1024  # Convertendo KB para bytes
file_index = 0
file_count = 1
current_file_name = f"arquivo_{file_index}.txt"
current_file = open(current_file_name, "w")
current_file_size = 0
first_combination = None  

def sanitize_filename(filename):
    # Remove caracteres inválidos para nomes de arquivos
    return re.sub(r'[<>:"/\|?*]', 'â', filename)

# Gerar todas as combinações possíveis de 5 caracteres
combinations = itertools.product(characters, repeat=tamanho_digitos)

for combination in combinations:
    combination_str = ''.join(combination) + "\n"
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
