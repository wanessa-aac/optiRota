import networkx as nx
import queue
import math
import logging
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict
try:
    # Execução como módulo do pacote src
    from .structures import PriorityQueue, reconstruct_path
    from .utils import euclidean_distance
except Exception:
    # Execução direta a partir da raiz do projeto
    from structures import PriorityQueue, reconstruct_path
    from utils import euclidean_distance

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def dijkstra(graph, start, end: Optional[str] = None, max_iterations: int = 10000) -> Dict[str, Any]:
    """
    Implementa o algoritmo de Dijkstra para encontrar o caminho mais curto entre dois nós.
    
    Usa uma PriorityQueue (heap) para relaxar vizinhos e encontrar o caminho ótimo.
    
    Args:
        graph: Grafo direcionado (NetworkX DiGraph ou similar)
        start: Nó de origem
        end: Nó de destino
        max_iterations: Limite máximo de iterações para evitar loops infinitos
        
    Returns:
        Dict contendo:
        - 'distance': distância total do caminho mais curto
        - 'path': lista de nós do caminho mais curto
        - 'distances': dicionário de distâncias de start para todos os nós
        - 'predecessors': dicionário de predecessores para reconstrução do caminho
        
    Raises:
        ValueError: Se start ou end não existem no grafo
        RuntimeError: Se o grafo é desconexo ou excede max_iterations
    """
    logging.info("Iniciando algoritmo de Dijkstra: %s -> %s", start, end)
    
    # Validação de entrada
    if start not in graph.nodes:
        raise ValueError(f"Nó de origem '{start}' não existe no grafo")
    if end is not None and end not in graph.nodes:
        raise ValueError(f"Nó de destino '{end}' não existe no grafo")
    
    # Inicialização
    distances = {node: math.inf for node in graph.nodes}
    distances[start] = 0
    predecessors = {node: None for node in graph.nodes}
    visited = set()
    
    # PriorityQueue para relaxar vizinhos (prioridade = distância)
    pq = PriorityQueue()
    pq.insert(start, 0)  # (nó, distância)
    
    iteration_count = 0
    
    while not pq.is_empty() and iteration_count < max_iterations:
        iteration_count += 1
        
        # Extrai o nó com menor distância
        current_node = pq.extract_min()
        
        # Se já visitamos este nó, pula
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        # Se chegamos ao destino, podemos parar
        if current_node == end:
            logging.info("Destino alcançado em %d iterações", iteration_count)
            break
        
        # Relaxa todos os vizinhos
        for neighbor in graph.neighbors(current_node):
            if neighbor in visited:
                continue
                
            # Obtém o peso da aresta
            edge_weight = graph[current_node][neighbor].get('weight', 1.0)
            
            # Calcula nova distância
            new_distance = distances[current_node] + edge_weight
            
            # Se encontrou um caminho mais curto, atualiza
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_node
                
                # Adiciona vizinho na fila de prioridade
                pq.insert(neighbor, new_distance)
                
                logging.debug("Relaxamento: %s -> %s, nova distância: %.2f", 
                            current_node, neighbor, new_distance)
    
    # Verifica se excedeu o limite de iterações
    if iteration_count >= max_iterations:
        raise RuntimeError(f"Algoritmo excedeu {max_iterations} iterações. Possível loop infinito.")
    
    if end is None:
    # Retorna apenas o dicionário de distâncias (igual ao networkx)
        return distances

    # Verifica se o destino foi alcançado
    if distances[end] == math.inf:
        raise RuntimeError(f"Não existe caminho de '{start}' para '{end}'. Grafo pode ser desconexo.")
    
    # Reconstrói o caminho usando Pilha (estruturas.reconstruct_path)
    path = reconstruct_path(predecessors, start, end)
    
    result = {
        'distance': distances[end],
        'path': path,
        'distances': distances,
        'predecessors': predecessors,
        'iterations': iteration_count,
        'nodes_visited': len(visited)
    }
    
    logging.info("Dijkstra concluído: distância=%.2f, caminho=%s, iterações=%d", 
                distances[end], path, iteration_count)
    
    return result


def dijkstra_all_pairs(graph, max_iterations: int = 10000) -> Dict[str, Dict[str, Any]]:
    """
    Executa Dijkstra para todos os pares de nós no grafo.
    
    Args:
        graph: Grafo direcionado
        max_iterations: Limite máximo de iterações por execução
        
    Returns:
        Dicionário aninhado com resultados para todos os pares
    """
    results = {}
    nodes = list(graph.nodes)
    
    logging.info("Executando Dijkstra para todos os pares (%d nós)", len(nodes))
    
    for i, start in enumerate(nodes):
        results[start] = {}
        for end in nodes:
            if start != end:
                try:
                    result = dijkstra(graph, start, end, max_iterations)
                    results[start][end] = {
                        'distance': result['distance'],
                        'path': result['path']
                    }
                except RuntimeError as e:
                    logging.warning("Sem caminho de %s para %s: %s", start, end, str(e))
                    results[start][end] = None
    
    logging.info("Dijkstra all-pairs concluído")
    return results


def a_star(graph, start, end, max_iterations: int = 10000) -> Dict[str, Any]:
    """
    Implementa o algoritmo A* para encontrar o caminho mais curto entre dois nós.
    
    Usa uma heurística admissível (distância Euclidiana) para guiar a busca
    de forma mais eficiente que o Dijkstra tradicional.
    
    Fórmula: f(n) = g(n) + h(n)
    - g(n): custo real do caminho do início até n
    - h(n): heurística (distância Euclidiana de n até o objetivo)
    - f(n): função de avaliação total
    
    Args:
        graph: Grafo direcionado (NetworkX DiGraph ou similar)
        start: Nó de origem
        end: Nó de destino
        max_iterations: Limite máximo de iterações para evitar loops infinitos
        
    Returns:
        Dict contendo:
        - 'distance': distância total do caminho mais curto
        - 'path': lista de nós do caminho mais curto
        - 'g_costs': dicionário de custos g(n) para todos os nós
        - 'f_costs': dicionário de custos f(n) para todos os nós
        - 'predecessors': dicionário de predecessores para reconstrução do caminho
        - 'iterations': número de iterações executadas
        - 'nodes_visited': número de nós visitados
        - 'nodes_evaluated': número de nós avaliados (incluindo não visitados)
        
    Raises:
        ValueError: Se start ou end não existem no grafo
        RuntimeError: Se o grafo é desconexo ou excede max_iterations
    """
    logging.info("Iniciando algoritmo A*: %s -> %s", start, end)
    
    # Validação de entrada
    if start not in graph.nodes:
        raise ValueError(f"Nó de origem '{start}' não existe no grafo")
    if end not in graph.nodes:
        raise ValueError(f"Nó de destino '{end}' não existe no grafo")
    
    # Inicialização
    g_costs = {node: math.inf for node in graph.nodes}  # g(n) - custo real
    g_costs[start] = 0
    f_costs = {node: math.inf for node in graph.nodes}  # f(n) = g(n) + h(n)
    predecessors = {node: None for node in graph.nodes}
    visited = set()
    evaluated = set()  # nós que foram avaliados (incluindo não visitados)
    
    # PriorityQueue para nós a serem explorados (prioridade = f(n))
    open_set = PriorityQueue()
    
    # Calcula h(start) e f(start)
    start_node_data = graph.nodes[start]
    end_node_data = graph.nodes[end]
    
    # Cria objetos mock para a função euclidean_distance
    class MockNode:
        def __init__(self, lat, lon):
            self.lat = lat
            self.lon = lon
    
    start_mock = MockNode(start_node_data['lat'], start_node_data['lon'])
    end_mock = MockNode(end_node_data['lat'], end_node_data['lon'])
    
    h_start = euclidean_distance(start_mock, end_mock)
    f_costs[start] = g_costs[start] + h_start
    
    open_set.insert(start, f_costs[start])
    evaluated.add(start)
    
    iteration_count = 0
    
    while not open_set.is_empty() and iteration_count < max_iterations:
        iteration_count += 1
        
        # Extrai o nó com menor f(n)
        current_node = open_set.extract_min()
        
        # Se já visitamos este nó, pula
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        # Se chegamos ao destino, podemos parar
        if current_node == end:
            logging.info("Destino alcançado em %d iterações", iteration_count)
            break
        
        # Avalia todos os vizinhos
        for neighbor in graph.neighbors(current_node):
            if neighbor in visited:
                continue
                
            # Obtém o peso da aresta
            edge_weight = graph[current_node][neighbor].get('weight', 1.0)
            
            # Calcula novo custo g(n)
            tentative_g_cost = g_costs[current_node] + edge_weight
            
            # Se encontrou um caminho melhor para o vizinho
            if tentative_g_cost < g_costs[neighbor]:
                # Atualiza custos
                g_costs[neighbor] = tentative_g_cost
                predecessors[neighbor] = current_node
                
                # Calcula h(n) para o vizinho
                neighbor_node_data = graph.nodes[neighbor]
                neighbor_mock = MockNode(neighbor_node_data['lat'], neighbor_node_data['lon'])
                h_neighbor = euclidean_distance(neighbor_mock, end_mock)
                
                # Calcula f(n) = g(n) + h(n)
                f_costs[neighbor] = g_costs[neighbor] + h_neighbor
                
                # Adiciona vizinho na fila de prioridade
                open_set.insert(neighbor, f_costs[neighbor])
                evaluated.add(neighbor)
                
                logging.debug("A* avaliação: %s -> %s, g=%.2f, h=%.2f, f=%.2f", 
                            current_node, neighbor, g_costs[neighbor], h_neighbor, f_costs[neighbor])
    
    # Verifica se excedeu o limite de iterações
    if iteration_count >= max_iterations:
        raise RuntimeError(f"Algoritmo A* excedeu {max_iterations} iterações. Possível loop infinito.")
    
    # Verifica se o destino foi alcançado
    if g_costs[end] == math.inf:
        raise RuntimeError(f"Não existe caminho de '{start}' para '{end}'. Grafo pode ser desconexo.")
    
    # Reconstrói o caminho usando Pilha (estruturas.reconstruct_path)
    path = reconstruct_path(predecessors, start, end)
    
    result = {
        'distance': g_costs[end],  # distância real (g-cost do destino)
        'path': path,
        'g_costs': g_costs,
        'f_costs': f_costs,
        'predecessors': predecessors,
        'iterations': iteration_count,
        'nodes_visited': len(visited),
        'nodes_evaluated': len(evaluated)
    }
    
    logging.info("A* concluído: distância=%.2f, caminho=%s, iterações=%d, visitados=%d, avaliados=%d", 
                g_costs[end], path, iteration_count, len(visited), len(evaluated))
    
    return result


def get_shortest_path_info(result: Dict[str, Any]) -> str:
    """
    Retorna uma string formatada com informações do caminho mais curto.
    
    Args:
        result: Resultado do algoritmo dijkstra ou A*
        
    Returns:
        String formatada com informações do caminho
    """
    if not result['path']:
        return "Nenhum caminho encontrado"
    
    path_str = " -> ".join(map(str, result['path']))
    
    # Verifica se é resultado do A* (tem nodes_evaluated)
    if 'nodes_evaluated' in result:
        return (f"Distância: {result['distance']:.2f}\n"
                f"Caminho: {path_str}\n"
                f"Iterações: {result['iterations']}\n"
                f"Nós visitados: {result['nodes_visited']}\n"
                f"Nós avaliados: {result['nodes_evaluated']}")
    else:
        return (f"Distância: {result['distance']:.2f}\n"
                f"Caminho: {path_str}\n"
                f"Iterações: {result['iterations']}\n"
                f"Nós visitados: {result['nodes_visited']}")

def vrp_solver(graph, orders, capacity: int = 100, time_window: Tuple[int, int] = (9, 11)) -> List[Any]:
    logging.info("Iniciando VRP Solver com %d pedidos", len(orders))

    # Fila FIFO com apenas pedidos dentro da janela de tempo
    fifo = queue.Queue()
    for order in orders:
        if time_window[0] <= order["time"] <= time_window[1]:
            fifo.put(order)

    route = [0]         # depósito = nó 0
    current_node = 0

    current_capacity = capacity

    while not fifo.empty():
        candidates = []
        # Coleta todos da fila para filtrar
        for _ in range(fifo.qsize()):
            order = fifo.get()
            if order["weight"] <= current_capacity:
                candidates.append(order)
            else:
                fifo.put(order)  # volta para a fila se não couber agora

        if not candidates:
            break

        # Escolhe vizinho mais próximo pelo peso da aresta
        next_order = min(
            candidates,
            key=lambda o: nx.shortest_path_length(
                graph, current_node, o["node"], weight="weight"
            )
        )

        # Atualiza rota
        route.append(next_order["node"])
        current_capacity -= next_order["weight"]
        current_node = next_order["node"]

        # Recoloca candidatos restantes na fila
        for order in candidates:
            if order["id"] != next_order["id"]:
                fifo.put(order)

    # Volta para o depósito
    route.append(0)
    logging.info("Rota finalizada: %s", route)
    return route
