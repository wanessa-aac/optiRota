import os
import math
import random
import pytest
import networkx as nx
import osmnx as ox

# Configuração de variáveis de ambiente
DATA_OSM = os.getenv("DATA_OSM", "data/090925maceio_ponta_verde.osm")
INTERMEDIATE_MAX_RATIO = float(os.getenv("INTERMEDIATE_MAX_RATIO", "0.20"))
WEIGHT_REL_TOL = float(os.getenv("REL_TOL", "1e-3"))
MAX_EDGES_TO_SAMPLE = int(os.getenv("MAX_EDGES_TO_SAMPLE", "300"))

# HELPERS (funções auxiliares)

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcula a distância haversine entre dois pontos geográficos."""
    R = 6371000.0  # Raio da Terra em metros
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def load_graph() ->nx.DiGraph:
    """Carrega o grafo direcionado a partir do arquivo OSM."""
    if not os.path.exists(DATA_OSM):
        pytest.skip(f"Arquivo OSM não encontrado em: {DATA_OSM}")
    
    from src.graph import build_graph
    from src.parser_osm import parse_osm

    parsed = parse_osm(DATA_OSM)
    G = build_graph(parsed)
    if not isinstance(G, nx.DiGraph):
        pytest.fail("O grafo retornado não é um networkx.DiGraph")
        
    return G

# Tests

def test_graph_is_directed_and_weighted():
    G = load_graph()
    assert G.is_directed(), "O grafo deve ser direcionado."
    assert G.number_of_nodes() > 0, "O grafo deve ter nós."
    assert G.number_of_edges() > 0, "O grafo deve ter arestas."
    for u, v, data in G.edges(data=True):
        assert "weight" in data, f"Aresta ({u}->{v}) sem atributo de 'weight'."
        assert isinstance(data["weight"], (int, float)), f"O peso da aresta ({u}->{v}) deve ser um número."
        assert data["weight"] >= 0, f"Peso negativo na aresta ({u}->{v})."

def test_connectivity_no_isolates_and_single_wcc():
    G = load_graph()
    isolated = [n for n in G.nodes if G.in_degree(n) + G.out_degree(n) == 0]
    assert not isolated, f"Há nós isolados: {isolated[:10]} (até 10)."
    wccs = list(nx.weakly_connected_components(G))
    giant = max(wccs, key=len)
    coverage = len(giant) / G.number_of_nodes()
    assert coverage >= 0.95, f"O maior componente cobre apenas {coverage:.1%} (esperado >= 95%)."

def test_absence_of_intermediate_nodes_degree2_ratio():
    G = load_graph()
    UG = G.to_undirected()
    deg = dict(UG.degree())
    deg2_nodes = sum(1 for d in deg.values() if d == 2)
    ratio = deg2_nodes / len(deg) if deg else 0
    assert ratio <= INTERMEDIATE_MAX_RATIO, f"Razão de nós de grau-2 = {ratio:.1%} excede o máximo ({INTERMEDIATE_MAX_RATIO:.0%})."

def test_edge_weights_match_haversine_with_tolerance():
    G = load_graph()
    # Exige que os nós tenham atributos lon e lat
    sample_nodes = list(G.nodes())[:50]
    if not all(("lat" in G.nodes[n] and "lon" in G.nodes[n]) for n in sample_nodes):
        pytest.skip("Nó(s) não possuem 'lat' e 'lon'.")
    edges = list(G.edges(data=True))
    random.shuffle(edges)
    edges = edges[:min(len(edges), MAX_EDGES_TO_SAMPLE)]
    for u, v, data in edges:
        lat1, lon1 = G.nodes[u]["lat"], G.nodes[u]["lon"]
        lat2, lon2 = G.nodes[v]["lat"], G.nodes[v]["lon"]
        expected = haversine(lat1, lon1, lat2, lon2)
        got = float(data.get("weight", float("nan")))
        assert math.isclose(got, expected, rel_tol=WEIGHT_REL_TOL), (
            f"Peso errado na aresta ({u}->{v}): obtido {got:.3f}, esperado {expected:.3f}"
        )
    
def test_access_and_oneway_filters_if_present():
    G = load_graph()
    has_access_attr = any("access" in d for _, _, d in G.edges(data=True))
    if has_access_attr:
        priv = [(u, v) for u, v, d in G.edges(data=True) if d.get("access") == "private"]
        assert not priv, f"Arestas com access=private encontradas: {priv[:5]}"
