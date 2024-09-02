import tkinter as tk
from tkinter import filedialog

def abrir_arquivo():
    # Abre o diálogo para seleção de arquivo
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo", 
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    
    # Verifica se um arquivo foi selecionado
    if caminho_arquivo:
        with open(caminho_arquivo, 'r') as arquivo:
            conteudo = arquivo.read()
            print(conteudo)  # Aqui você pode manipular o conteúdo do arquivo como preferir

# Configura a janela principal do Tkinter
janela = tk.Tk()
janela.title("Leitor de Arquivo")
janela.geometry("400x300")

# Adiciona um botão para abrir o arquivo
botao_abrir = tk.Button(janela, text="Abrir Arquivo", command=abrir_arquivo)
botao_abrir.pack(pady=20)

# Inicia o loop principal do Tkinter
janela.mainloop()
