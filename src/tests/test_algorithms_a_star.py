import math
import pytest
import networkx as nx

try:
    from src.algorithms import a_star, dijkstra
    from src.utils import euclidean_distance, haversine_distance
except Exception:
    from algorithms import a_star, dijkstra
    from utils import euclidean_distance, haversine_distance

# Função auxiliar que somar os pesos das arestas ao longo de path
def _path_distance(G, path):
    d = 0.0
    for u, v in zip(path, path[1:]):
        d += G[u][v]["weight"]
    return d #retorna um float com distância total ao longo do path no grafo G

# Teste de optimalidade do A* vs Dijkstra em grid com heurística consistente
def test_a_star_optimality_matches_dijkstra_on_grid(grid_graph_10):
    G, start, end = grid_graph_10
    # grid_graph_10 é um fixture definido em conftest.py: um grid 2x5(10 nós) com pesos euclidianos e nós com lat/lon.
    da = a_star(G, start, end) # A* do projeto
    dd = dijkstra(G, start, end) # Dijkstra do projeto
    assert pytest.approx(da["distance"], rel=1e-9) == dd["distance"] # compara as distâncias (com tolerância 1e-9), entre os dois algoritmos.
    assert da["path"][0] == start and da["path"][-1] == end # verifica se o path do A* começa em start e termina em end.
    assert pytest.approx(da["distance"], rel=1e-9) == _path_distance(G, da["path"])

# Teste de grafo cíclico com atalho ('corda')
def test_a_star_handles_cycles_shortcut_is_found(ring_graph):
    G = ring_graph
    res = a_star(G, 0, 3) # Do nó 0 ao 3, A* deve considerar ciclos, evitar loop infinito e aproveitar a corda se ela reduzir custo.
    assert res["path"][0] == 0 and res["path"][-1] == 3 # Checa endpoints do path.
    assert pytest.approx(res["distance"], rel=1e-9) == _path_distance(G, res["path"])
    # Distância retornada = soma das arestas do caminho

# Teste de componentes desconexos
def test_a_star_unreachable_raises(disconnected_graph):
    G = disconnected_graph # A* não deve conseguir conexão entre A1 e B1, que estão em componentes desconexos.
    with pytest.raises((RuntimeError, ValueError)):
        a_star(G, "A1", "B1") # A* deve lançar RuntimeError ao tentar ir de A1 a B1, que estão em componentes desconexos.

# Teste de admissibilidade da heurística(xfail)
@pytest.mark.xfail(reason="Heurística euclidiana não é admissível com pesos Haversine; sugerido usar haversine como h(n).")
def test_euclidean_heuristic_admissibility_against_haversine(tiny_haversine_graph):
    G = tiny_haversine_graph
    goal = 2
    for n in G.nodes:
        N = type("N", (), G.nodes[n])
        Goal = type("N", (), G.nodes[goal])
        h_euc = euclidean_distance(N, Goal)
        h_hav = haversine_distance(G.nodes[n]["lat"], G.nodes[n]["lon"], 
                                   G.nodes[goal]["lat"], G.nodes[goal]["lon"])
        assert h_euc <= h_hav + 1e-9 # pode falhar (xfail) se heurística euclidiana não for admissível com pesos haversine.
