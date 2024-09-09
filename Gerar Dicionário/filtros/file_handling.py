# file_handling.py

import os
import re

def sanitize_filename(filename):
    """
    Remove ou substitui caracteres inválidos para nomes de arquivos.
    """
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def create_new_file(file_name):
    """
    Cria um novo arquivo e retorna o objeto de arquivo e o tamanho inicial (0).
    """
    current_file = open(file_name, "w")
    return current_file, 0
