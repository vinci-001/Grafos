import pandas as pd

def formatar_cnpj(cnpj):
  
    cnpj = cnpj.zfill(14)  # Garante que o CNPJ tenha 14 dígitos, preenchendo com zeros à esquerda se necessário
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

def formatar_cnpj_csv(arquivo_entrada, arquivo_saida):
    
    # Carregar o arquivo CSV em um DataFrame, assumindo que a primeira linha é o cabeçalho
    df = pd.read_csv(arquivo_entrada)

    # Verificar se a coluna 'CNPJ' existe no DataFrame
    if 'CNPJ' not in df.columns:
        print("Erro: A coluna 'CNPJ' não foi encontrada no arquivo CSV.")
        return

    # Aplicar a formatação aos números de CNPJ
    df['CNPJ'] = df['CNPJ'].apply(formatar_cnpj)

    # Salvar o DataFrame formatado em um novo arquivo CSV
    df.to_csv(arquivo_saida, index=False)

    print(f"O arquivo com CNPJs formatados foi salvo como {arquivo_saida}")

def converter_nomes_para_maiusculo(arquivo_entrada, arquivo_saida):
    # Carrega o arquivo CSV
    df = pd.read_csv(arquivo_entrada)

    # Converte os valores da coluna "nome" para maiúsculas
    df['nome'] = df['nome'].str.upper()

    # Salva o arquivo CSV atualizado
    df.to_csv(arquivo_saida, index=False)

    print(f"Todos os nomes da coluna 'nome' foram convertidos para maiúsculas e salvos em {arquivo_saida}.")


def remove_columns(input_csv, output_csv, columns_to_remove):
    # Lê o CSV de entrada
    df = pd.read_csv(input_csv)
    
    # Remove as colunas especificadas
    df.drop(columns=columns_to_remove, inplace=True, errors='ignore')
    
    # Salva o DataFrame modificado em um novo CSV
    df.to_csv(output_csv, index=False)
    print(f"Colunas {columns_to_remove} removidas e arquivo salvo como {output_csv}.")

def salvar_graus_maiores(G, file_path_links, csv_filename='graus_maiores.csv'):
    # Carregar os dados do arquivo links.csv
    df_links = pd.read_csv(file_path_links)

    # Obter o conjunto de vértices presentes em links.csv
    vertices_links = set(df_links['nome'])
    
    # Calcular os graus dos vértices
    graus = dict(G.degree())

    # Filtrar os vértices que estão no arquivo links.csv
    graus_filtrados = {v: graus[v] for v in vertices_links if v in graus}

    # Criar um DataFrame com os resultados
    df_graus = pd.DataFrame(list(graus_filtrados.items()), columns=['Vértice', 'Grau'])
    
    # Ordenar o DataFrame pelo grau em ordem decrescente
    df_graus = df_graus.sort_values(by='Grau', ascending=False)
    
    # Salvar o DataFrame como CSV
    df_graus.to_csv(csv_filename, index=False)
    print(f"CSV com graus maiores salvo como {csv_filename}.")

def remove_duplicates_by_name(file_path, output_path):
    """
    Remove duplicatas do arquivo CSV com base na coluna 'nome', mantendo a primeira ocorrência de cada nome.
    
    :param file_path: Caminho para o arquivo CSV original.
    :param output_path: Caminho para salvar o arquivo CSV limpo.
    """
    # Carregar o arquivo CSV
    df = pd.read_csv(file_path)
    
    # Remover duplicatas, mantendo apenas a primeira ocorrência de cada nome
    df_cleaned = df.drop_duplicates(subset='nome', keep='first')
    
    # Salvar o arquivo CSV limpo
    df_cleaned.to_csv(output_path, index=False)
    
    print("Duplicatas removidas com sucesso!")

def converter_nomes_para_maiusculo(input_csv, output_csv):
    try:
        # Lê o arquivo CSV
        df = pd.read_csv(input_csv)

        # Verifica se a coluna 'nome' existe
        if 'nome' not in df.columns:
            raise ValueError(f"A coluna 'nome' não foi encontrada no arquivo {input_csv}.")

        # Converte todos os valores da coluna 'nome' para maiúsculo
        df['nome'] = df['nome'].str.upper()

        # Salva o novo arquivo CSV com os nomes em maiúsculo
        df.to_csv(output_csv, index=False)
        print(f"Nomes convertidos para maiúsculo e salvos em {output_csv}.")
    
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

# Exemplo de uso

# Exemplo de uso
# formatar_cnpj_csv('seu_arquivo.csv', 'seu_arquivo_formatado.csv')
