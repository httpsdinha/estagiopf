import itertools

caracteres = '''abc'defghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]}{|;:",.<>/?\`~©®™§°†‡±π∞µΩáéíóúàèìòùâêîôûäëïöüãõñçÇ£¥€₩₹∞√∑∏≠≤≥≡±×÷⊗⊕ñÑß '''
nome_arquivo = 'dicionario1.txt'

# Abra o arquivo para escrita fora do loop
with open(nome_arquivo, 'w', encoding='utf-8') as f:
    # Gere combinações
    for i in range(1, 7):
        for combinacao in itertools.product(caracteres, repeat=i):
            combinacao_str = ''.join(combinacao)
            # Escreva cada combinação no arquivo
            f.write(combinacao_str + '\n')

print(f'Arquivo {nome_arquivo} gerado com sucesso!')
