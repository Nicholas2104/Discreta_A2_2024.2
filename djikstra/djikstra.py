import pandas as pd
import numpy as np

df = pd.read_csv("Dados_Estatisticos.csv", sep=';')

# Removendo linhas nulas
df_clean = df.dropna(subset=['DECOLAGENS','AEROPORTO_DE_ORIGEM_SIGLA', 'AEROPORTO_DE_DESTINO_SIGLA', 
                     'DISTANCIA_VOADA_KM'])

df_cleaner = df_clean.query("AEROPORTO_DE_ORIGEM_SIGLA != 'N/I' and AEROPORTO_DE_DESTINO_SIGLA != 'N/I'")

# Cria uma lista de todos os aeroportos
airports = list(set(df_cleaner['AEROPORTO_DE_ORIGEM_SIGLA']).union(set(df_cleaner['AEROPORTO_DE_DESTINO_SIGLA'])))
airport_idx = {airport: idx for idx, airport in enumerate(airports)} # Mapeia aeroportos para índices

# Inicializa a matriz com infinito nas entradas
n = len(airports)
adj_matrix = np.full((n,n), float('inf'))

# Preenche as entradas da matriz com as distâncias
for _, row in df_cleaner.iterrows():
    origin = airport_idx[row['AEROPORTO_DE_ORIGEM_SIGLA']]
    destination = airport_idx[row['AEROPORTO_DE_DESTINO_SIGLA']]
    if row['DECOLAGENS'] and row['DISTANCIA_VOADA_KM'] > 0:
        distance = row['DISTANCIA_VOADA_KM']//row['DECOLAGENS'] # Distancia por decolagem (DISTANCIA_VOADA_KM é acumulada mensalmente)
        adj_matrix[origin][destination] = distance 

def dijkstra(adj_matrix: list[list[float]], start_idx: int, end_idx: int) -> tuple[list[str], float]:
    n = len(adj_matrix)
    distances = [float('inf')] * n # Armazenando as distancias como infinito
    distances[start_idx] = 0 # Distancia do vertice inicial inicializada como zero
    visited = [False] * n
    predecessors = [None] * n

    for _ in range(n):
        # Escolhe o nó com a menor distancia que ainda nao foi visitado 
        min_distance = float('inf')
        min_node = None

        for i in range(n):
            if not visited[i] and distances[i] < min_distance:
                min_distance = distances[i]
                min_node = i

        if min_node is None: # nós disponiveis ja visitados
            break 

        visited[min_node] = True

        # Atualiza a distancia para os vizinhos do nó que esta sendo observado
        for neighbor in range(n):
            if adj_matrix[min_node][neighbor] != float('inf') and not visited[neighbor]:
                new_dist = distances[min_node] + adj_matrix[min_node][neighbor]
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    predecessors[neighbor] = min_node

    # Constroi o caminho
    path = []
    current = end_idx
    while current is not None:
        path.insert(0, airports[current], )
        current = predecessors[current]

    if distances[end_idx] == float('inf'):
        # Nenhum caminho foi encontrado
        return None, float('inf') 
    return path, distances[end_idx] # retorna o caminho e a distancia em km

origin_airport = input("Insira o aeroporto de origem:")
destination_airport = input("Insira o aeroporto de destino:")

start_idx = airport_idx[origin_airport]
end_idx = airport_idx[destination_airport]

path, length = dijkstra(adj_matrix, start_idx, end_idx)

if path:
    print(f"A rota mais curta de {origin_airport} para {destination_airport} é: {path}")
    print(f"A distância total é: {length}")
else:
    print(f"Nenhum caminho foi encontrado!")
