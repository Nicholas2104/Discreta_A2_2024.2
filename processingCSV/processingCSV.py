import pandas as pd
import numpy as np

# Essa função processa o CSV com os voos
def processing_csv_ford_fulkerson(archive_path : str, capacity_column : str):

    # carrega o dataframe do local indicado
    df = pd.read_csv(archive_path, sep=';')

    # filtra os voos regulares (comuns)
    df = df[df["GRUPO_DE_VOO"] == 'REGULAR']

    # tira a media por decolagem de capacidade
    df[capacity_column] /= df['DECOLAGENS']

    # agrupa os voos de todas os meses e anos pela media da capacidade
    df = df.groupby(["AEROPORTO_DE_ORIGEM_SIGLA", 'AEROPORTO_DE_DESTINO_SIGLA'])[capacity_column].mean().reset_index()

    # filtra voo que tem mais de 0 de capacidade e arredonda caso tenha algum fracionario
    df = df[df[capacity_column] > 0]
    df[capacity_column] = np.round(df[capacity_column])

    # filtra valores N/A
    df = df.dropna().reset_index()

    # Cria uma lista com os aeroportos e uma matrix quadrada com o mesmo tamanho
    airports_list = sorted(pd.unique(df[['AEROPORTO_DE_ORIGEM_SIGLA', 'AEROPORTO_DE_DESTINO_SIGLA']].values.ravel()))
    adj_matrix = np.full((len(airports_list),len(airports_list)), 0)

    # Completa a matrix de adjacencia com as capacidades
    for _, row in df.iterrows():
        origin_idx = airports_list.index(row['AEROPORTO_DE_ORIGEM_SIGLA'])
        dest_idx = airports_list.index(row['AEROPORTO_DE_DESTINO_SIGLA'])
        adj_matrix[origin_idx, dest_idx] = row[capacity_column]

    df.to_csv('ford_fulkerson/dados_limpos.csv')
    np.save("ford_fulkerson/adj_matrix.npy", adj_matrix)
    np.save("ford_fulkerson/airports_list.npy", airports_list)

    return adj_matrix, airports_list

processing_csv_ford_fulkerson("processingCSV/Dados_Estatisticos.csv", 'ASSENTOS')