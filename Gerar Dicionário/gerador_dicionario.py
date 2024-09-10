import tkinter as tk
from tkinter import filedialog, messagebox, StringVar, Entry, Button, OptionMenu, Label, Spinbox
import os
from filtros.filters import *
from filtros.file_handling import sanitize_filename, create_new_file
from filtros.combinacoes import generate_combinations
import threading

def validate_inputs():
    """Valida as entradas do usuário."""
    try:
        tamanho_digitos = int(digits_entry.get())
        if tamanho_digitos <= 0:
            raise ValueError("A quantidade de dígitos deve ser um número positivo.")
        
        max_file_size_mb = int(file_size_spinbox.get())
        if max_file_size_mb <= 0:
            raise ValueError("O tamanho máximo do arquivo deve ser um número positivo.")
        
        if not base_filename_entry.get():
            raise ValueError("O nome base do arquivo não pode estar vazio.")
        
        return True
    except ValueError as ve:
        messagebox.showerror("Erro de Validação", str(ve))
        return False

def generate_dictionaries():
    """Gera os arquivos de dicionário com base nas entradas do usuário."""
    if not validate_inputs():
        return

    status_label.config(text="Gerando dicionário...")
    root.update_idletasks()

    characters = characters_var.get()
    if characters == "Personalizado":
        characters = custom_characters_entry.get()
    else:
        characters = options.get(characters, "")

    tamanho_digitos = int(digits_entry.get())
    max_file_size_mb = int(file_size_spinbox.get())
    max_file_size = max_file_size_mb * 1024 * 1024

    choice = filter_var.get()
    filter_func = select_filter(choice)

    save_path = save_path_var.get()
    base_filename = base_filename_entry.get()

    if not save_path:
        messagebox.showerror("Erro", "Selecione um local para salvar os arquivos.")
        return

    if not base_filename:
        messagebox.showerror("Erro", "Digite um nome base para os arquivos.")
        return

    def write_to_file(file, combination_str):
        """Escreve no arquivo e gerencia o tamanho do arquivo."""
        combination_size = len(combination_str.encode('utf-8'))
        file.write(combination_str)
        return combination_size

    def process_combinations():
        file_index = 0
        current_file_name = ""
        current_file = None
        current_file_size = 0

        file_index = 0
        current_file_name = os.path.join(save_path, f"{base_filename}_{file_index}.txt")
        current_file, current_file_size = create_new_file(current_file_name)

        try:
            for combination_str in generate_combinations(characters, tamanho_digitos, filter_func):
                combination_size = write_to_file(current_file, combination_str)
                current_file_size += combination_size

                if current_file_size >= max_file_size:
                    current_file.close()
                    new_file_name = os.path.join(save_path, f"{base_filename}_{file_index}.txt")
                    os.rename(current_file_name, sanitize_filename(new_file_name))

                    file_index += 1
                    current_file_name = os.path.join(save_path, f"{base_filename}_{file_index}.txt")
                    current_file, current_file_size = create_new_file(current_file_name)

            if current_file_size > 0:
                new_file_name = os.path.join(save_path, f"{base_filename}_{file_index}.txt")
                os.rename(current_file_name, sanitize_filename(new_file_name))

            messagebox.showinfo("Sucesso", f"Combinações geradas e distribuídas em {file_index + 1} arquivos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        finally:
            status_label.config(text="Pronto")

    # Executa a geração em uma thread separada para manter a interface responsiva
    threading.Thread(target=process_combinations).start()

def select_save_location():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        save_path_var.set(folder_selected)
        save_path_label.config(text=f"Diretório selecionado: {folder_selected}")

def select_filter(choice):
    filter_funcs = {
        'Apenas caracteres maiúsculos no início': uppercase_start,
        'Apenas números no início': start_number,
        'Apenas números no final': final_number,
        'Apenas caracteres especiais no início': start_especiais,
        'Apenas caracteres especiais no final': final_especiais,
        'Nenhum filtro': None
    }
    return filter_funcs.get(choice, None)

def update_characters_entry(*args):
    selected_option = characters_var.get()
    if selected_option in options:
        custom_characters_entry.delete(0, tk.END)
        custom_characters_entry.insert(0, options[selected_option])

def setup_ui():
    global root, characters_var, options, custom_characters_entry, digits_entry, file_size_spinbox, filter_var, base_filename_entry, save_path_var, save_path_label, status_label

    root.title("Gerador de Dicionário")
    root.geometry("700x400")

    main_frame = tk.Frame(root, padx=15, pady=15)
    main_frame.pack(fill="both", expand=True)

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
    custom_characters_entry = Entry(main_frame, width=40)
    custom_characters_entry.grid(row=1, column=1, sticky="ew", pady=5)

    tk.Label(main_frame, text="Quantidade de dígitos:").grid(row=2, column=0, sticky="w", pady=5)
    digits_entry = Entry(main_frame, width=40)
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

    tk.Label(main_frame, text="Nome base do arquivo:").grid(row=5, column=0, sticky="w", pady=5)
    base_filename_entry = Entry(main_frame, width=40)
    base_filename_entry.grid(row=5, column=1, sticky="ew", pady=5)

    tk.Label(main_frame, text="Diretório selecionado:").grid(row=6, column=0, sticky="w", pady=5)
    save_path_var = StringVar()
    save_path_label = Label(main_frame, text=":")
    save_path_label.grid(row=6, column=1, sticky="w", pady=5)

    save_path_button = Button(main_frame, text="Escolher Local do Arquivo", command=select_save_location)
    save_path_button.grid(row=7, column=0, columnspan=2, pady=10)

    generate_button = Button(main_frame, text="Gerar Dicionário", command=generate_dictionaries)
    generate_button.grid(row=8, column=0, columnspan=2, pady=10)

    status_label = Label(main_frame, text="Pronto para gerar dicionário")
    status_label.grid(row=9, column=0, columnspan=2, pady=10)

    characters_var.trace("w", update_characters_entry)
    update_characters_entry()

root = tk.Tk()
setup_ui()
root.mainloop()
