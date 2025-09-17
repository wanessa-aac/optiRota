import pytest
import math
import networkx as nx

# Esperado: src/algorithms.py define dijkstra(G, source)
try:
    from src.algorithms import dijkstra
except Exception as e:
    dijkstra = None
    IMPORT_ERROR = e
else:
    IMPORT_ERROR = None


@pytest.fixture
def graph_simple():
    """Grafo dirigido simples com pesos não-negativos e caminho alternativo pior."""
    G = nx.DiGraph()
    edges = [
        ("A", "B", 1.0),
        ("B", "C", 2.0),
        ("A", "C", 5.0),  # pior que A->B->C (1+2=3 < 5)
        ("C", "D", 1.5),
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    return G


@pytest.fixture
def graph_cyclic():
    """Grafo dirigido com ciclo A->B->C->A e dois caminhos para D."""
    G = nx.DiGraph()
    edges = [
        ("A", "B", 2.0),
        ("B", "C", 2.0),
        ("C", "A", 2.0),  # ciclo
        ("B", "D", 1.0),  # melhor rota a partir de A
        ("C", "D", 10.0),
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    return G


def _run_dijkstra(G, source):
    """Executa seu dijkstra e normaliza para um dict de distâncias."""
    if dijkstra is None:
        pytest.skip(f"Função dijkstra não encontrada: {IMPORT_ERROR}")
    out = dijkstra(G, source)
    dist = out[0] if isinstance(out, tuple) else out
    return dict(dist)


def test_non_negative_distances(graph_simple):
    """Distâncias devem ser não-negativas se todas as arestas são não-negativas."""
    dist = _run_dijkstra(graph_simple, "A")
    for node, d in dist.items():
        assert d >= 0, f"Distância negativa em {node}: {d}"


def test_matches_networkx_shortest_paths(graph_simple):
    """Comparação de optimalidade com a referência do NetworkX."""
    dist = _run_dijkstra(graph_simple, "A")
    gold = nx.single_source_dijkstra_path_length(graph_simple, "A", weight="weight")
    assert set(dist.keys()) == set(gold.keys())
    for k in gold:
        assert math.isclose(dist[k], gold[k], rel_tol=1e-9, abs_tol=1e-12)


def test_cyclic_graph_optimality(graph_cyclic):
    """Mesmo com ciclo, distâncias devem bater com a referência."""
    dist = _run_dijkstra(graph_cyclic, "A")
    gold = nx.single_source_dijkstra_path_length(graph_cyclic, "A", weight="weight")
    assert set(dist.keys()) == set(gold.keys())
    for k in gold:
        assert math.isclose(dist[k], gold[k], rel_tol=1e-9, abs_tol=1e-12)
