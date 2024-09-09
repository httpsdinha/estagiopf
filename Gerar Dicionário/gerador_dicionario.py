import tkinter as tk
from tkinter import messagebox, StringVar, Entry, Button, OptionMenu, Label, Spinbox
from filtros.filters import *
from filtros.file_handling import sanitize_filename, create_new_file
from filtros.combinacoes import generate_combinations  # Importação correta

def generate_dictionaries():
    status_label.config(text="Gerando dicionário...")
    root.update_idletasks()

    characters = characters_var.get()

    if characters in options.keys() and characters != "Personalizado":
        characters = options[characters]

    if characters == "Personalizado":
        characters = custom_characters_entry.get()

    tamanho_digitos = int(digits_entry.get())
    max_file_size_mb = int(file_size_spinbox.get())
    max_file_size = max_file_size_mb * 1024 * 1024

    choice = filter_var.get()
    filter_func = select_filter(choice)

    file_index = 0
    current_file_name = f"arquivo_{file_index}.txt"
    current_file, current_file_size = create_new_file(current_file_name)

    try:
        for combination_str in generate_combinations(characters, tamanho_digitos, filter_func):
            combination_size = len(combination_str.encode('utf-8'))

            if current_file_size + combination_size > max_file_size:
                current_file.close()
                file_index += 1
                current_file_name = f"arquivo_{file_index}.txt"
                current_file, current_file_size = create_new_file(current_file_name)

            current_file.write(combination_str)
            current_file_size += combination_size

        current_file.close()
        messagebox.showinfo("Sucesso", f"Combinações geradas e distribuídas em {file_index + 1} arquivos.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    finally:
        status_label.config(text="Pronto")

def update_characters_entry(*args):
    """
    Atualiza a entrada de caracteres personalizados com base na seleção.
    """
    selected_option = characters_var.get()
    if selected_option in options:
        custom_characters_entry.delete(0, tk.END)
        custom_characters_entry.insert(0, options[selected_option])

# Interface gráfica
root = tk.Tk()
root.title("Gerador de Dicionário")
root.geometry("400x400")

main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.grid(row=0, column=0, sticky="nsew")

main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=2)

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
custom_characters_entry = Entry(main_frame)
custom_characters_entry.grid(row=1, column=1, sticky="ew", pady=5)

tk.Label(main_frame, text="Quantidade de dígitos:").grid(row=2, column=0, sticky="w", pady=5)
digits_entry = Entry(main_frame)
digits_entry.grid(row=2, column=1, sticky="ew", pady=5)

tk.Label(main_frame, text="Tamanho máximo do arquivo em MB:").grid(row=3, column=0, sticky="w", pady=5)
file_size_spinbox = Spinbox(main_frame, from_=10, to=1000, increment=1, width=6)
file_size_spinbox.delete(0, tk.END)
file_size_spinbox.insert(0, 250)
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
