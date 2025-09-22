import math
import pytest
import networkx as nx

alg = pytest.importorskip("src.algorithms", reason="src.algorithms não disponível ou não encontrado(verifique os requisitos).")
dijkstra = getattr(alg, "dijkstra", None)
assert callable(dijkstra), "src.algorithms.dijkstra não encontrado ou não é chamável."

def _run_dijkstra(G, source):
    out = dijkstra(G, source)
    if isinstance(out, tuple) and len(out) >= 2:
        dist, prev = out[0], out[1]
    else:
        dist, prev = (out, None)
    return dict(dist), prev

@pytest.fixture
def graph_simple():
    G = nx.DiGraph()
    edges = [("A", "B", 1.0), ("B", "C", 2.0), ("A", "C", 5.0), ("C", "D", 1.5)]
    for u, v, w in edges: G.add_edge(u, v, weight=w)
    return G

@pytest.fixture
def graph_cyclic():
    G = nx.DiGraph()
    edges = [("A", "B", 2.0), ("B", "C", 2.0), ("C", "A", 2.0), ("B", "D", 1.0), ("C", "D", 10.0)]
    for u, v, w in edges: G.add_edge(u, v, weight=w)
    return G

@pytest.fixture
def graph_unreachable():
    G = nx.DiGraph()
    G.add_edge("A", "B", weight=1.0); G.add_edge("B", "C", weight=1.0)
    G.add_node("Z")  # Nó Z desconectado
    return G

@pytest.fixture
def graph_zero_weight():
    G = nx.DiGraph()
    G.add_edge("A", "B", weight=0.0); G.add_edge("B", "C", weight=0.0); G.add_edge("A", "C", weight=1.0)
    return G

def test_non_negative_distances(graph_simple):
    dist, _= _run_dijkstra(graph_simple, "A")
    assert all(d >= 0 for d in dist.values())

def test_matches_networkx_shortest_paths(graph_simple):
    dist, _= _run_dijkstra(graph_simple, "A")
    gold = nx.single_source_dijkstra_path_length(graph_simple, "A", weight="weight")
    assert set(dist.keys()) == set(gold.keys())
    for k in gold:
        assert math.isclose(dist[k], gold[k], rel_tol=1e-9, abs_tol=1e-12)

def test_cyclic_graph_optimality(graph_cyclic):
    dist, _= _run_dijkstra(graph_cyclic, "A")
    gold = nx.single_source_dijkstra_path_length(graph_cyclic, "A", weight="weight")
    assert set(dist.keys()) == set(gold.keys())
    for k in gold:
        assert math.isclose(dist[k], gold[k], rel_tol=1e-9, abs_tol=1e-12)

def test_zero_weight_edges(graph_zero_weight):
    dist, _= _run_dijkstra(graph_zero_weight, "A")
    gold = nx.single_source_dijkstra_path_length(graph_zero_weight, "A", weight="weight")
    assert set(dist.keys()) == set(gold.keys())
    for k in gold:
        assert math.isclose(dist[k], gold[k], rel_tol=1e-9, abs_tol=1e-12)