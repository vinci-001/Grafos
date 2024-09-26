import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def exportar_graus_mais_que_um(G, output_csv='vertices_maior_que_um.csv'):
    # Calcular o grau de cada vértice no grafo
    graus = dict(G.degree())

    # Filtrar vértices com grau maior que 1
    graus_filtrados = {vertice: grau for vertice, grau in graus.items() if grau > 1}

    # Ordenar os vértices pelo grau de forma decrescente
    graus_ordenados = dict(sorted(graus_filtrados.items(), key=lambda item: item[1], reverse=True))

    # Criar um DataFrame com os vértices e seus graus
    df_graus = pd.DataFrame(list(graus_ordenados.items()), columns=['Vértice', 'Grau'])

    # Exportar para CSV
    df_graus.to_csv(output_csv, index=False)

    print(f"CSV com vértices de maior grau salvo como {output_csv}.")

    return df_graus

def create_graph(G, node_sizes):
    fig, ax = plt.subplots(figsize=(12, 8))

    # Layout Spring com valor de k ajustado para maior distância entre os nós
    pos = nx.spring_layout(G, k=5.0)  # Aumente o valor de k para ajustar a distância
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='lightblue', ax=ax)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.7, ax=ax)
    nx.draw_networkx_labels(G, pos, labels={node: i+1 for i, node in enumerate(G.nodes)}, font_size=10, font_weight='bold', ax=ax)

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red', font_size=8, ax=ax)

    ax.set_title("Grafo de Instituições e Fornecedores")
    ax.axis('off')

    plt.show()

def grafo(file_path1, file_path2):
    try:
        # Lê os arquivos
        df1 = pd.read_csv(file_path1)
        df2 = pd.read_csv(file_path2)

        # Verifica se as colunas necessárias estão presentes
        required_columns_df1 = {'institucao', 'valorContrato', 'CNPJ', 'nome'}
        if not required_columns_df1.issubset(df1.columns):
            raise ValueError(f"O arquivo {file_path1} não contém as colunas necessárias.")
        
        required_columns_df2 = {'CNPJ', 'nome'}
        if not required_columns_df2.issubset(df2.columns):
            raise ValueError(f"O arquivo {file_path2} não contém as colunas necessárias.")

        G = nx.Graph()
        
        # Remove duplicatas dos dataframes
        df1 = df1.drop_duplicates(subset=['CNPJ', 'nome'])
        df2 = df2.drop_duplicates(subset=['CNPJ', 'nome'])

        # Adiciona arestas entre instituições e fornecedores com base no valor do contrato
        for index, row in df1.iterrows():
            instituicao = row['institucao']
            fornecedor = row['nome']
            valor_contrato = row['valorContrato']

            if pd.notna(instituicao) and pd.notna(fornecedor) and valor_contrato > 0:
                if G.has_edge(instituicao, fornecedor):
                    # Se a aresta já existe, soma o valor do contrato
                    G[instituicao][fornecedor]['weight'] += valor_contrato
                else:
                    # Caso contrário, adiciona a nova aresta com o valor do contrato
                    G.add_edge(instituicao, fornecedor, weight=valor_contrato)

        # Adiciona novos vértices e arestas com base no arquivo links.csv
        for index, row in df2.iterrows():
            cnpj = row['CNPJ']
            nome = row['nome']

            if pd.notna(cnpj) and pd.notna(nome):
                # Encontra o nome correspondente no df1 com o mesmo CNPJ
                matched_rows = df1[df1['CNPJ'] == cnpj]
                for _, matched_row in matched_rows.iterrows():
                    nome_correspondente = matched_row['nome']
                    if nome_correspondente in G.nodes:
                        G.add_edge(nome, nome_correspondente)  # Conecta o nome do links.csv ao nome do CG-CONTRATOS.csv

        # Imprime estatísticas do grafo
        print(f"Número total de arestas: {G.number_of_edges()}")
        print(f"Número total de vértices: {G.number_of_nodes()}")

        node_sizes = []
        vertex_values = {}

        # Calcula os tamanhos dos nós baseados nos valores de contrato
        for vertex in G.nodes:
            if vertex in df1['institucao'].values:
                vertex_value = df1[df1['institucao'] == vertex]['valorContrato'].max()
            elif vertex in df1['nome'].values:
                vertex_value = df1[df1['nome'] == vertex]['valorContrato'].sum()
            else:
                vertex_value = 1  # Valor mínimo
            
            vertex_values[vertex] = vertex_value
            node_sizes.append(300 + (vertex_value / max(vertex_values.values())) * 1000)

        # Gera o grafo
        create_table(G, df1, df2, csv_filename='vertices_tabela.csv')
        create_graph(G, node_sizes)
        exportar_graus_mais_que_um(G)

    except Exception as e:
        print(f"Erro ao processar o grafo: {e}")

def create_table(G, df1, df2, csv_filename='vertices_tabela.csv'):
    vertices = list(G.nodes)
    cpfs_cnpjs = []

    for vertex in vertices:
        if vertex in df1['institucao'].values:  # Verifica se é uma instituição
            cpf_cnpj = df1[df1['institucao'] == vertex]['CNPJ'].iloc[0]
            cpfs_cnpjs.append(cpf_cnpj)
        elif vertex in df1['nome'].values:  # Se for pessoa (dono de CNPJ)
            cpf_cnpj = df1[df1['nome'] == vertex]['CNPJ'].iloc[0]  # Usa o CNPJ do arquivo 1
            cpfs_cnpjs.append(cpf_cnpj)
        elif vertex in df2['nome'].values:  # Se for nome do arquivo links
            cpf_cnpj = df2[df2['nome'] == vertex]['CNPJ'].iloc[0]  # Usa o CNPJ do arquivo 2
            cpfs_cnpjs.append(cpf_cnpj)
        else:
            cpf_cnpj = 'Não disponível'
            cpfs_cnpjs.append(cpf_cnpj)

    # Cria o DataFrame com os dados
    vertex_df = pd.DataFrame({
        'Número': range(1, len(vertices) + 1),
        'Vértice': vertices,
        'CPF/CNPJ': cpfs_cnpjs
    })

    # Salva o DataFrame como CSV
    vertex_df.to_csv(csv_filename, index=False)
    print(f"Tabela de vértices salva como {csv_filename}.")

def executar_grafo():
    arquivo1 = 'CG-CONTRATOS.csv'
    arquivo2 = 'combined_coisas_links.csv'
    
    grafo(arquivo1, arquivo2)

