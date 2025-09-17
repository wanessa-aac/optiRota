import math
import logging
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict
try:
    # Execução como módulo do pacote src
    from .structures import PriorityQueue, reconstruct_path
except Exception:
    # Execução direta a partir da raiz do projeto
    from structures import PriorityQueue, reconstruct_path

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


def get_shortest_path_info(result: Dict[str, Any]) -> str:
    """
    Retorna uma string formatada com informações do caminho mais curto.
    
    Args:
        result: Resultado do algoritmo dijkstra
        
    Returns:
        String formatada com informações do caminho
    """
    if not result['path']:
        return "Nenhum caminho encontrado"
    
    path_str = " -> ".join(map(str, result['path']))
    return (f"Distância: {result['distance']:.2f}\n"
            f"Caminho: {path_str}\n"
            f"Iterações: {result['iterations']}\n"
            f"Nós visitados: {result['nodes_visited']}")
