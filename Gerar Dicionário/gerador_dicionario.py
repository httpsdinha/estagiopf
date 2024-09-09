import itertools
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, StringVar, OptionMenu  

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


def generate_dictionaries():
    # Atualiza o status na interface
    status_label.config(text="Gerando dicionário...")
    root.update_idletasks()  # Atualiza a interface
    
    characters = characters_var.get()
    if characters == "Personalizado":
        characters = custom_characters_entry.get().strip()
        if not characters:
            messagebox.showerror("Erro", "Por favor, digite os caracteres personalizados.")
            status_label.config(text="Erro durante a geração.")
            return
    
    tamanho_digitos = digits_entry.get().strip()
    max_file_size_mb = file_size_entry.get().strip()
    if not tamanho_digitos.isdigit() or not max_file_size_mb.isdigit():
        messagebox.showerror("Erro", "Por favor, digite valores válidos para o tamanho dos dígitos e o tamanho do arquivo.")
        status_label.config(text="Erro durante a geração.")
        return
    
    tamanho_digitos = int(tamanho_digitos)
    max_file_size_mb = int(max_file_size_mb)
    max_file_size_kb = max_file_size_mb * 1024
    max_file_size = max_file_size_kb * 1024

    choice = filter_var.get()

    # Define o filtro com base na escolha do usuário
    filter_func = {
        'Apenas caracteres maiúsculos no início': uppercase_start,
        'Apenas números no início': start_number,
        'Apenas números no final': final_number,
        'Apenas caracteres especiais no início': start_especiais,
        'Apenas caracteres especiais no final': final_especiais,
        'Nenhum filtro': lowercase_letters
    }.get(choice, None)
        
    # Inicializando variáveis
    file_index = 0
    file_count = 1
    current_file_name = f"arquivo_{file_index}.txt"
    
    try:
        with open(current_file_name, "w") as current_file:
            current_file_size = 0
            first_combination = None 
            
            # Gerar todas as combinações possíveis de X caracteres
            for combination_str in generate_combinations(characters,tamanho_digitos, filter_func):
                combination_size = len(combination_str.encode('utf-8'))  # Tamanho da combinação em bytes
                
                if current_file_size == 0:
                    first_combination = sanitize_filename(combination_str.strip())  # Armazena a primeira combinação
                    first_combination = combination_str.strip()  # Armazena a primeira combinação

                if current_file_size + combination_size > max_file_size:
                    last_combination = sanitize_filename(combination_str.strip())
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
                new_file_name = sanitize_filename(new_file_name)
                os.rename(current_file_name, new_file_name)

            messagebox.showinfo("Sucesso", f"Combinações geradas e distribuídas entre {file_count} arquivos, renomeados com o primeiro e último dígito de cada.")
    except Exception as e:
        status_label.config(text="Erro durante a geração.")
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Interface Gráfica

root = tk.Tk()
root.title = "Gerador de Dicionário"

tk.Label(root, text="Escolha as caracteres: ").pack()

characters_var = StringVar(value="Padrão")
options = {
    "Padrão": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*()_-+=?",
    "Números": "0123456789",
    "Letras maiúsculas": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "Letras minúsculas": "abcdefghijklmnopqrstuvwxyz",
    "Caracteres especiais": "@#*_-",
    "Personalizado": ""
}

character_menu = OptionMenu(root, characters_var, *options.keys())
character_menu.pack()

tk.Label(root, text="Digite os caracteres personalizados (se selecionado 6):").pack()
custom_characters_entry = tk.Entry(root)
custom_characters_entry.pack()

tk.Label(root, text="Quantidade de dígitos:").pack()
digits_entry = tk.Entry(root)
digits_entry.pack()

tk.Label(root, text="Tamanho máximo do arquivo em MB:").pack()
file_size_entry = tk.Entry(root)
file_size_entry.pack()

tk.Label(root, text="Escolha o filtro:").pack()
filter_var = StringVar(value='Nenhum filtro')
filter_options = [
    'Apenas caracteres maiúsculos no início',
    'Apenas números no início',
    'Apenas números no final',
    'Apenas caracteres especiais no início',
    'Apenas caracteres especiais no final',
    'Nenhum filtro'
]
filter_menu = OptionMenu(root, filter_var, *filter_options)
filter_menu.pack()


tk.Button(root, text="Gerar Dicionário", command=generate_dictionaries).pack()

# Status Label
status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()