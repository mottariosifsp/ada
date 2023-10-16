nome_arquivo_entrada = 'name_replacements.txt'
nome_arquivo_saida = 'name_replacements-filtered.txt'

# Abre o arquivo de entrada para leitura e o arquivo de saída para escrita
with open(nome_arquivo_entrada, 'r') as arquivo_entrada, open(nome_arquivo_saida, 'w') as arquivo_saida:
    # Lê cada linha do arquivo de entrada
    for linha in arquivo_entrada:
        # Verifica se a linha contém a palavra "migrations"
        if '/migrations/' not in linha:
            # Se não contiver, escreve a linha no arquivo de saída
            arquivo_saida.write(linha)

# Exibe uma mensagem de conclusão
print(f"A filtragem foi concluída. Linhas que mencionavam 'migrations' foram removidas em {nome_arquivo_saida}.")
