import tkinter as tk
from tkinter import filedialog
import hashlib

def gerar_hash(conteudo, algoritmo):
    hash_obj = hashlib.new(algoritmo)
    hash_obj.update(conteudo)
    return hash_obj.hexdigest()

def abrir_arquivo():
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo", 
        filetypes=[("All files", "*.*")]
    )
    
    if caminho_arquivo:
        with open(caminho_arquivo, 'rb') as arquivo: 
            conteudo = arquivo.read()
            algoritmo_selecionado = var_algoritmo.get()
            hash_resultado = gerar_hash(conteudo, algoritmo_selecionado)
            print(f"{algoritmo_selecionado.upper()}: {hash_resultado}")
            entry_hash.delete(0, tk.END)  
            entry_hash.insert(0, hash_resultado)  

def copiar_hash():
    janela.clipboard_clear()
    janela.clipboard_append(entry_hash.get())
    janela.update() 
    print("Hash copiada para a área de transferência!")

#Organização da Tela
janela = tk.Tk()
janela.title("Leitor de Arquivo e Gerador de Hash")
janela.geometry("450x230")
frame_principal = tk.Frame(janela)
frame_principal.pack(expand=True)
frame_opcao = tk.Frame(frame_principal)
frame_opcao.pack(pady=10)


#Menu de Algoritmos Hash
var_algoritmo = tk.StringVar(value="sha256")
algoritmos = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]
label_opcao = tk.Label(frame_opcao, text="Escolha o algoritmo de hash:")
label_opcao.pack(side=tk.LEFT, padx=5)
menu_algoritmo = tk.OptionMenu(frame_opcao, var_algoritmo, *algoritmos)
menu_algoritmo.pack(side=tk.LEFT, padx=5)

#Frame para organizar a barra de texto e o botão de copiar lado a lado
frame_hash = tk.Frame(frame_principal)
frame_hash.pack(pady=20)

#Campo de texto
entry_hash = tk.Entry(frame_hash, width=60) 
entry_hash.pack(side=tk.LEFT, padx=5)

#Botão
botao_copiar = tk.Button(frame_hash, text="Copiar", command=copiar_hash)
botao_copiar.pack(side=tk.LEFT, padx=5)

botao_abrir = tk.Button(frame_principal, text="Abrir Arquivo", command=abrir_arquivo)
botao_abrir.pack(pady=10)


janela.mainloop()
