import math
import pytest
import networkx as nx

# Garante que temos A* do projeto; pulamos o teste se não tiveros requisitos
alg = pytest.importorskip(
    "src.algorithms", reason = "Não foi possível importar src.algorithms(verifique os requisitos)."
)
a_star = getattr(alg, "a_star", None)
assert callable(a_star), "src.algorithms.a_star não encontrado ou não é chamável."

# Helpers para criar grafos de teste

def _distance_matrix_via_astar(G, nodes):
    """
    Retorna uma matriz de distâncias {u: {v: dist}} entre 'nodes' usando o A* do projeto.
    - Usa a API do A*: a_star(G, u, v) -> {"distance": float, "path": [..]}
    - Distância de u para u é 0.0 (por convenção).
    """
    dist = {u: {} for u in nodes}
    for u in nodes:
        for v in nodes:
            if u == v:
                dist[u][v] = 0.0
            else:
                res = a_star(G, u, v)
                d = res["distance"]
                # Sanidade mínima: distância deve ser positiva e finita
                assert d >= 0.0 and math.isfinite(d), f"Distância inválida A* {u}->{v}: {d}"
                dist[u][v] = d
    return dist

def _nn_vrp(dist, depot, customers):
    """
    VRP 1-veículo por heurística de Vizinho Mais Próximo.
    - dist: matriz {u: {v: custo}}
    - depot: nó inicial/final
    - customers: lista de nós a visitar
    Retorna uma rota [depot, ..., depot] cobrindo todos os customers exatamente 1x.
    """
    unvisited = set(customers)
    route = [depot]
    cur = depot
    while unvisited:
        # escolhe o cliente ainda não visitado mais próximo de 'cur'
        nxt = min(unvisited, key=lambda c: dist[cur][c])
        route.append(nxt)
        unvisited.remove(nxt)
        cur = nxt
    route.append(depot)
    return route

def _route_cost(dist, route):
    """ Soma os custos da matrix 'dist' ao longo da 'route' (lista de nós). """
    return sum(dist[route[i]][route[i+1]] for i in range(len(route)-1))

# Teste principal de integração OPT-20

def test_pipeline_graph_astar_vrp(grid_graph_10):
    """
    Pipeline:
    1) Recebe grafo dirigido e pesado (grid_graph_10) [10 nós].
    2) Seleciona 1 depósito + 3 entregas.
    3) Constrói matriz de distâncias via A*.
    4) Monta rota NN-VRP e valida propriedades básicas.
    """
    G, start, end = grid_graph_10

    # Seleciona 1 depósito + 3 entregas (clientes)
    depot = start # canto superior esquerdo do grid
    customers = [1, 3, 7] # três nós distintos do grid
    nodes = [depot] + customers

    # 1) Matriz de distâncias via A*
    dist = _distance_matrix_via_astar(G, nodes)

    # 2) Rota via heurística VRP simples (1 veículo, NN)
    route = _nn_vrp(dist, depot, customers)

    # 3) Asserções de integração
    # - Rota começa e termina no depósito
    assert route[0] == depot and route[-1] == depot
    # - Rota visita todos os clientes exatamente 1x
    assert set(route[1:-1]) == set(customers) and len(route[1:-1]) == len(customers)
    # - Custo da rota é positivo e finito
    total = _route_cost(dist, route)
    assert total > 0.0 and math.isfinite(total)
    # Para grid pequeno, um limite superior folgado ajuda a capturar explosões de custo
    assert total < 1e8, f"Custo anormalmente alto: {total}"

   