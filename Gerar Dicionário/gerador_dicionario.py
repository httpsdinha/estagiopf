import itertools
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, StringVar, OptionMenu, Label, Entry, Button, Spinbox

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

def generate_dictionaries():
    # Atualiza o status na interface
    status_label.config(text="Gerando dicionário...")
    root.update_idletasks()  # Atualiza a interface
    
    characters = characters_var.get()
    if characters == "Personalizado":
        characters = custom_characters_entry.get()
    
    tamanho_digitos = int(digits_entry.get())
    max_file_size_mb = int(file_size_spinbox.get())
    max_file_size_kb = max_file_size_mb * 1024  # Convertendo MB para KB
    max_file_size = max_file_size_kb * 1024  # Convertendo KB para bytes

    choice = filter_var.get()

    # Define o filtro com base na escolha do usuário
    if choice == 'Apenas caracteres maiúsculos no início':
        filter_func = uppercase_start
    elif choice == 'Apenas números no início':
        filter_func = start_number
    elif choice == 'Apenas números no final':
        filter_func = final_number
    elif choice == 'Apenas caracteres especiais no início':
        filter_func = start_especiais
    elif choice == 'Apenas caracteres especiais no final':
        filter_func = final_especiais
    elif choice == 'Nenhum filtro':
        filter_func = lowercase_letters
    else:
        filter_func = None
        
    # Inicializando variáveis
    file_index = 0
    file_count = 1
    current_file_name = f"arquivo_{file_index}.txt"
    current_file = open(current_file_name, "w")
    current_file_size = 0
    first_combination = None 

    try:
        # Gerar todas as combinações possíveis de X caracteres
        for combination_str in generate_combinations(characters,tamanho_digitos, filter_func):
            combination_size = len(combination_str.encode('utf-8'))  # Tamanho da combinação em bytes
            
            if current_file_size == 0:
                first_combination = sanitize_filename(combination_str.strip())  # Armazena a primeira combinação
                first_combination = combination_str.strip()  # Armazena a primeira combinação

            if current_file_size + combination_size > max_file_size:
                # Renomeia o arquivo com base na primeira e última combinação
                current_file.close()
                last_combination = sanitize_filename(combination_str.strip())  # Última combinação
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

def update_characters_entry(*args):
    selected_option = characters_var.get()
    if selected_option in options:
        custom_characters_entry.delete(0, tk.END)
        custom_characters_entry.insert(0, options[selected_option])

# Interface Gráfica
root = tk.Tk()
root.title("Gerador de Dicionário")
root.geometry("600x400")  # Define o tamanho da janela

# Layout principal
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.grid(row=0, column=0, sticky="nsew")

# Configura as colunas e linhas do grid
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=2)
main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=1)
main_frame.rowconfigure(2, weight=1)
main_frame.rowconfigure(3, weight=1)
main_frame.rowconfigure(4, weight=1)
main_frame.rowconfigure(5, weight=1)

tk.Label(main_frame, text="Escolha os caracteres:").grid(row=0, column=0, sticky="w")
characters_var = StringVar(value="Padrão")
options = {
    "Padrão": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*()_-+=?",
    "Números": "0123456789",
    "Letras maiúsculas": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "Letras minúsculas": "abcdefghijklmnopqrstuvwxyz",
    "Caracteres especiais": "@#*_-",
    "Personalizado": ""
}

character_menu = OptionMenu(main_frame, characters_var, *options.keys())
character_menu.grid(row=0, column=1, sticky="ew")

tk.Label(main_frame, text="Digite os caracteres personalizados:").grid(row=1, column=0, sticky="w", pady=5)
custom_characters_entry = Entry(main_frame, width=40)
custom_characters_entry.grid(row=1, column=1, sticky="ew", pady=5)

tk.Label(main_frame, text="Quantidade de dígitos:").grid(row=2, column=0, sticky="w", pady=5)
digits_entry = Entry(main_frame, width=6)
digits_entry.grid(row=2, column=1, sticky="ew", pady=5)

tk.Label(main_frame, text="Tamanho máximo do arquivo em MB:").grid(row=3, column=0, sticky="w", pady=5)
file_size_spinbox = Spinbox(main_frame, from_=10, to=1000, increment=1, width=6)
file_size_spinbox.delete(0, tk.END)  # Limpa o valor existente
file_size_spinbox.insert(0, 250)    # Valor padrão de 250 MB
file_size_spinbox.grid(row=3, column=1, sticky="ew", pady=5)

tk.Label(main_frame, text="Escolha o filtro:").grid(row=4, column=0, sticky="w", pady=5)
filter_var = StringVar(value='Nenhum filtro')
filter_options = [
    'Apenas caracteres maiúsculos no início',
    'Apenas números no início',
    'Apenas números no final',
    'Apenas caracteres especiais no início',
    'Apenas caracteres especiais no final',
    'Nenhum filtro'
]
filter_menu = OptionMenu(main_frame, filter_var, *filter_options)
filter_menu.grid(row=4, column=1, sticky="ew")

generate_button = Button(main_frame, text="Gerar Dicionário", command=generate_dictionaries)
generate_button.grid(row=5, column=0, columnspan=2, pady=10)

status_label = Label(main_frame, text="Pronto para gerar dicionário")
status_label.grid(row=6, column=0, columnspan=2, pady=10)

characters_var.trace("w", update_characters_entry)
update_characters_entry()

root.mainloop()
