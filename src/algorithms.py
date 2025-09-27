import os
import csv
import networkx as nx
import queue
import time
import math
import logging
import json
from typing import Dict, List, Tuple, Optional, Any, Set, Iterable
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
    """Implementa o algoritmo de Dijkstra para encontrar o caminho mais curto entre dois nós.
    
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
        
    Example:
        >>> import networkx as nx
        >>> G = nx.DiGraph()
        >>> G.add_edge('A', 'B', weight=1.0)
        >>> G.add_edge('B', 'C', weight=2.0)
        >>> result = dijkstra(G, 'A', 'C')
        >>> print(f"Distância: {result['distance']}, Caminho: {result['path']}")
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

# === OPT-17: Pré-cálculo VRP (A*) ===
# Objetivo: pré-computar distâncias dirigidas entre pares de nós usando A* e salvar em CSV (data/distances.csv)
# Notas:
#  - Usa cache persistente (reaproveita o CSV existente) e um cache em memória simples (dict).
#  - Amostra 10–20 nós por padrão para não estourar memória/tempo durante o desenvolvimento.
#  - Formato do CSV (long format): source,target,distance_meters,path_nodes(JSON)

def _ensure_data_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)

def _build_distance_matrix(graph, nodes: List[str]) -> Dict[int, Dict[int, float]]:
    """
    Constrói matriz de distâncias robusta usando Dijkstra/A*.
    
    Args:
        graph: Grafo NetworkX
        nodes: Lista de nós para calcular distâncias
        
    Returns:
        Matriz de distâncias como dicionário aninhado
    """
    distance_matrix = {}
    n = len(nodes)
    
    logging.info("Calculando matriz de distâncias %dx%d", n, n)
    
    for i, node_i in enumerate(nodes):
        distance_matrix[i] = {}
        
        for j, node_j in enumerate(nodes):
            if i == j:
                distance_matrix[i][j] = 0.0
            else:
                try:
                    # Tenta A* primeiro (mais eficiente)
                    result = a_star(graph, node_i, node_j)
                    distance_matrix[i][j] = result['distance']
                except:
                    try:
                        # Fallback para Dijkstra
                        result = dijkstra(graph, node_i, node_j)
                        distance_matrix[i][j] = result['distance']
                    except:
                        # Se ambos falharem, usa distância euclidiana como estimativa
                        if hasattr(graph.nodes[node_i], 'get') and hasattr(graph.nodes[node_j], 'get'):
                            lat1, lon1 = graph.nodes[node_i].get('lat', 0), graph.nodes[node_i].get('lon', 0)
                            lat2, lon2 = graph.nodes[node_j].get('lat', 0), graph.nodes[node_j].get('lon', 0)
                            from src.utils import euclidean_distance
                            distance_matrix[i][j] = euclidean_distance(
                                type('Node', (), {'lat': lat1, 'lon': lon1}),
                                type('Node', (), {'lat': lat2, 'lon': lon2})
                            )
                        else:
                            distance_matrix[i][j] = float('inf')
    
    logging.info("Matriz de distâncias calculada com sucesso")
    return distance_matrix

def _load_done_pairs(cache_path: str) -> Set[Tuple[str, str]]:
    """
    Lê data/distances.csv e retorna um set com (source, target) já calculados.
    """
    done: Set[tuple[str, str]] = set()
    if not os.path.exists(cache_path):
        return done
    try:
        with open(cache_path, "r", newline="", encoding="utf-8") as f:
            rdr = csv.DictReader(f)
            for row in rdr:
                s, t = row.get("source"), row.get("target")
                if s and t:
                    done.add((s, t))
    except Exception as e:
        logging.error("Falha ao ler cache CSV (%s): %s", cache_path, e)
    return done

def precompute_distances(
    graph, 
    nodes: Optional[Iterable[str]] = None,
    k_sample: int = 20,
    out_path: str = "data/distances.csv",
    resume: bool = True,
    chunk_size: int = 200,
    max_iterations: int = 10000,
) -> int:
    """
    Pré-computa distâncias dirigidas entre pares de nós usando A* e salva em CSV.

    Args:
      graph: DiGraph com 'lat'/'lon' nos nós e 'weight' nas arestas
      nodes: subconjunto de nós (ids). Se None, amostra k_sample nós aleatórios.
      k_sample: tamanho da amostra quando nodes=None
      out_path: caminho do CSV de saída (data/distances.csv)
      resume: se True, pula pares já presentes no CSV (retomada)
      chunk_size: quantas linhas escrever por flush
      max_iterations: limite de iterações do A*

    Returns:
      Quantidade de NOVAS linhas gravadas no CSV.
    """
    logging.info("Iniciando pré-calculo de distâncias com A*")
    _ensure_data_dir(out_path)

# 1) Seleção de nós
    if nodes is None:
        all_nodes = list(graph.nodes)
        if not all_nodes:
            raise ValueError("Grafo vazio - nenhum nó disponível")
        k = min(k_sample, len(all_nodes))
        # amostra simples para não explodir custo durante desenvolvimento
        import random
        nodes_sel = list(map(str, random.sample(all_nodes, k)))
        logging.info("Amostra automatica de %d nós", k)
    else:
        nodes_sel = [str(n) for n in nodes]
        logging.info("Usando %d nós fornecidos", len(nodes_sel))

    # 2) Cache persistente (retomada)
    done_pairs = _load_done_pairs(out_path) if resume else set()
    if resume:
        logging.info("Pares já computados no CSV (cache): %d", len(done_pairs))

    # 3) CSV (append) e cabeçalho
    file_exists = os.path.exists(out_path)
    written_now = 0
    buffer_rows: list[dict[str, Any]] = []

    # 4) Cache em memória (mesma execução)
    mem_cache: dict[tuple[str, str], tuple[Optional[float], Optional[list[str]]]] = {}
    pairs = [(u, v) for u in nodes_sel for v in nodes_sel if u != v]
    logging.info("Total de pares a avaliar: %d", len(pairs))

    fieldnames = ["source", "target", "distance_meters", "path_nodes"]

    try:
        f = open(out_path, "a", newline="", encoding="utf-8")
    except Exception as e:
        logging.error("Não foi possível abrir o arquivo de saída: %s", e)
        raise
    with f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        for idx, (u, v) in enumerate(pairs, start=1):
            if resume and (u, v) in done_pairs:
                continue
            if (u, v) in mem_cache:
                dist, path = mem_cache[(u, v)]
            else:
                # 5) Executa A* com tratamento de erros
                try:
                    res = a_star(graph, u, v, max_iterations=max_iterations)
                    dist = float(res["distance"])
                    path = [str(n) for n in res["path"]]
                except Exception as e:
                    logging.debug("Sem caminho ou falha A*: %s -> %s (%s)", u, v, e)
                    dist, path = None, None
                mem_cache[(u, v)] = (dist, path)
            
            row = {
                "source": u,
                "target": v,
                "distance_meters": "NA" if dist is None else round(dist, 6),
                "path_nodes": "NA" if path is None else json.dumps(path, ensure_ascii=False),
            }
            buffer_rows.append(row)

            # 6) Flush por chunk
            if len(buffer_rows) >= chunk_size:
                writer.writerows(buffer_rows)
                f.flush()
                written_now += len(buffer_rows)
                buffer_rows.clear()
                logging.info("Gravadas %d linhas (parcial)", written_now)
            
        # flush final
        if buffer_rows:
            writer.writerows(buffer_rows)
            f.flush()
            written_now += len(buffer_rows)
            buffer_rows.clear()
            logging.info("Gravadas %d linhas (final)", written_now)
    logging.info("Finalizado. Novas linhas gravadas: %d | CSV: %s", written_now, out_path)
    return written_now

def _vrp_nearest_neighbor(graph, orders, depot_node, capacity, distance_matrix):
    """
    Heurística Nearest Neighbor para VRP.
    Constrói rotas visitando sempre o cliente mais próximo.
    """
    routes = []
    unrouted = orders.copy()
    
    while unrouted:
        current_route = [depot_node]
        current_capacity = 0.0
        
        while unrouted:
            best_customer = None
            best_distance = float('inf')
            
            for order in unrouted:
                if current_capacity + order.get("weight", 0) <= capacity:
                    # Calcula distância do último nó da rota para este cliente
                    last_node = current_route[-1]
                    try:
                        # Encontra índice do último nó na matriz
                        last_idx = None
                        for i, node in enumerate([depot_node] + [o["node"] for o in orders]):
                            if node == last_node:
                                last_idx = i
                                break
                        
                        # Encontra índice do cliente
                        client_idx = None
                        for i, node in enumerate([depot_node] + [o["node"] for o in orders]):
                            if node == order["node"]:
                                client_idx = i
                                break
                        
                        if last_idx is not None and client_idx is not None:
                            distance = distance_matrix[last_idx][client_idx]
                            if distance < best_distance:
                                best_distance = distance
                                best_customer = order
                    except:
                        continue
            
            if best_customer is None:
                break
                
            # Adiciona cliente à rota
            current_route.append(best_customer["node"])
            current_capacity += best_customer.get("weight", 0)
            unrouted.remove(best_customer)
        
        # Fecha a rota retornando ao depósito
        current_route.append(depot_node)
        routes.append(current_route)
    
    return routes

def _calculate_route_distance(route, distance_matrix, depot_node, orders):
    """Calcula distância total de uma rota."""
    total_distance = 0.0
    for i in range(len(route) - 1):
        try:
            # Encontra índices na matriz
            from_idx = None
            to_idx = None
            all_nodes = [depot_node] + [o["node"] for o in orders]
            for j, node in enumerate(all_nodes):
                if node == route[i]:
                    from_idx = j
                if node == route[i + 1]:
                    to_idx = j
                if from_idx is not None and to_idx is not None:
                    break
            
            if from_idx is not None and to_idx is not None:
                total_distance += distance_matrix[from_idx][to_idx]
        except:
            continue
    
    return total_distance

def vrp_solver(
    graph: nx.DiGraph,
    orders: List[Dict],
    capacity: int = 100,
    time_window: Tuple[int, int] = (9, 11),
    distance_matrix: Optional[Dict[int, Dict[int, float]]] = None,
    depot_node: int = 0
) -> Dict[str, Any]:
    """
    Vehicle Routing Problem (VRP) solver com janelas de tempo (VRPTW simplificado).
    Usa matriz de distâncias pré-computada (A*) + heurística Vizinho Mais Próximo com Inserção.
    """

    start_time = time.time()
    logging.info("Iniciando VRP Solver com %d pedidos", len(orders))

    # -------------------------------
    # 1. Pré-processamento dos pedidos
    # -------------------------------
    valid_orders = []
    for order in orders:
        tw = order.get("time", order.get("time_window"))
        if isinstance(tw, tuple) and len(tw) == 2:
            start, end = tw
            if time_window[0] <= start and end <= time_window[1]:
                valid_orders.append(order)
        elif isinstance(tw, (int, float)):
            if time_window[0] <= tw <= time_window[1]:
                valid_orders.append(order)
        else:
            valid_orders.append(order)  # aceita sem restrição

    if not valid_orders:
        return {
            "routes": [],
            "total_distance": 0.0,
            "num_vehicles": 0,
            "unrouted_orders": orders,
            "route_details": [],
            "computation_time": time.time() - start_time,
            "distance_matrix_cache_hit": distance_matrix is not None
        }

    # -------------------------------
    # 2. Matriz de distâncias
    # -------------------------------
    distance_matrix_cache_hit = True
    if distance_matrix is None:
        distance_matrix_cache_hit = False
        nodes = [depot_node] + [o["node"] for o in valid_orders]
        # Cria matriz de distâncias robusta
        distance_matrix = _build_distance_matrix(graph, nodes)

    # -------------------------------
    # 3. VRP Solver Robusto
    # -------------------------------
    # Usa heurística Nearest Neighbor
    routes = _vrp_nearest_neighbor(graph, valid_orders, depot_node, capacity, distance_matrix)
    
    # -------------------------------
    # 4. Cálculo de métricas
    # -------------------------------
    route_details = []
    total_distance = 0.0
    
    for route in routes:
        if len(route) < 2:
            continue
            
        route_distance = _calculate_route_distance(route, distance_matrix, depot_node, valid_orders)
        total_distance += route_distance
        
        # Calcula capacidade usada
        capacity_used = 0.0
        orders_served = []
        for order in valid_orders:
            if order["node"] in route:
                capacity_used += order.get("weight", 0)
                orders_served.append(order.get("id", order["node"]))
        
        route_details.append({
            "route": route,
            "distance": route_distance,
            "capacity_used": capacity_used,
            "orders_served": len(orders_served),
            "orders": orders_served
        })

    # Identifica pedidos não roteados
    routed_nodes = set()
    for route in routes:
        routed_nodes.update(route)
    
    unrouted_orders = [order for order in valid_orders if order["node"] not in routed_nodes]

    result = {
        "routes": routes,
        "total_distance": total_distance,
        "num_vehicles": len(routes),
        "unrouted_orders": unrouted_orders,
        "route_details": route_details,
        "computation_time": time.time() - start_time,
        "distance_matrix_cache_hit": distance_matrix_cache_hit
    }

    logging.info("VRP finalizado: %d rotas, distância total = %.2f", len(routes), total_distance)
    return result
