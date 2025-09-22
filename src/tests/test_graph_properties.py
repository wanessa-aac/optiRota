import pytest
import networkx as nx

def _check_weights_non_negative(G):
    for u, v, data in G.edges(data=True):
        assert "weight" in data, f"Edge {u}->{v} sem 'weight'"
        assert data["weight"] >= 0, f"Peso negativo em {u}->{v}: {data['weight']}"

def test_grid_graph_properties(grid_graph_10):
    G, start, end = grid_graph_10
    assert isinstance(G, nx.DiGraph)
    assert G.number_of_nodes() == 10
    assert start in G and end in G
    _check_weights_non_negative(G)

def test_ring_graph_properties(ring_graph):
    G = ring_graph
    assert isinstance(G, nx.DiGraph)
    assert G.number_of_nodes() >= 5
    _check_weights_non_negative(G)

def test_disconnected_graph_properties(disconnected_graph):
    G = disconnected_graph
    assert isinstance(G, nx.DiGraph)
    # Deve ter pelo menos 2 componentes
    assert nx.number_weakly_connected_components(G) >= 2
    _check_weights_non_negative(G)

def test_tiny_haversine_weights(tiny_haversine_graph):
    G = tiny_haversine_graph
    # Pesos devem estar presentes e > 0
    for u, v, data in G.edges(data=True):
        assert data["weight"] > 0
        