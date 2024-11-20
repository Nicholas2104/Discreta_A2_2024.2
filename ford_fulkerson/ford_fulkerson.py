import numpy as np

# essa função aplica Deep-First Search no grafo de voos para encontrar uma caminho qualquer
def dfs(adj_matrix, airports_list, origin: str, destiny: str):

    # Encontram o indice do aeroporto de origem e destino na lista de aeroportos (devolve uma mensagem caso os aeroportos são sejam achados)    
    try:
        origin_index = airports_list.index(origin)
        destiny_index = airports_list.index(destiny)
    except ValueError:
        print("Aeroporto de destino ou origem errados")
        return None

    # Inicializa a lista que vai carregar o caminho final, a conjunto de vertices visitados e adiciona a origem nele
    path = [origin_index]
    visited_nodes = set()  # Use a set for faster membership checks
    visited_nodes.add(origin_index)

    # Esse bloco é o loop principal do algoritmo de bfs
    while path:
        # o vertice atual é o ultimo da lista que carrega o caminho
        current_node = path[-1] 

        # Se o vertice atual é o que queremos, retornamos o caminho
        if current_node == destiny_index:
            return path

        # Guarda os vizinhos ainda não visitados do vertice atual
        neighbors = [
            i for i in range(len(adj_matrix[current_node]))
            if adj_matrix[current_node][i] > 0 and i not in visited_nodes
        ]

        # Se a lista de vizinho não é vazia, atualiza as variaveis e continua o loop, se não volta um elemento na lista com o caminho e continua o loop
        if neighbors:
            next_node = neighbors[0]
            path.append(next_node)
            visited_nodes.add(next_node)
        else:
            path.pop()
    
    # Se o loop terminar sem retornar então não existe caminho e a função retorna None
    return None

# essa função aplica o algoritmo de Ford Fulkerson para encontrar o fluxo maximo entre dois aeroportos
def ford_fulkerson(archive_path: str, origin: str, destiny: str, capacity_column : str):

    # Carrega a matrix e a lista de aeroportos para a função bfs e inicializa a lista com as capacidades minimas de cada caminho
    adj_matrix = np.load("ford_fulkerson/adj_matrix.npy")
    airports_list = np.load("ford_fulkerson/airports_list.npy").tolist()
    airports_list
    minimum_capacities = []

    # Esse é o loop principal do algoritmo, onde vão sendo encontrados caminhos com a função dfs,
    # então a arestas são saturadas e as capacidades atualizadas para o que ainda está disponivel
    # até todos os caminhos estarem saturados e não existir mais caminhos com capacidade disponivel
    while True:

        # aplica dfs no grafo atual
        current_result = dfs(adj_matrix, airports_list, origin, destiny)

        # se não existir mais caminhos para o loop
        if current_result == None:
            break

        # inicializa a lista das capacidades e das arestas
        capacities = []
        edges = []

        # preenche as listas criadas
        for i in range(len(current_result)-1):
            capacities.append(adj_matrix[current_result[i]][current_result[i+1]])
            edges.append((current_result[i],current_result[i+1]))

        # encontra a capacidade minima e guarda ela na lista de capacidades minimas
        min_capacity = min(capacities)
        minimum_capacities.append(min_capacity)

        # atualiza as capacidades das arestas do caminho para o diferença entre a capacidade e o fluxo atual
        for i in edges:
            adj_matrix[i[0]][i[1]] = adj_matrix[i[0]][i[1]] - min_capacity

    # Printa e retorna o fluxo maximo
    max_flow = sum(minimum_capacities)
    print(f'O fluxo maximo entre {origin} e {destiny} é de {max_flow}')

    return max_flow

        

# aplica a função ford_fulkerson
origin = input('Insira o aeroporto fonte: ')
destiny = input('Insira o aeroporto destino: ')
ford_fulkerson("djikstra/Dados_Estatisticos.csv", origin, destiny, 'ASSENTOS')