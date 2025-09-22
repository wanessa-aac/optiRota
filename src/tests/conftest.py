# src/tests/conftest.py
# ============================================================
# Purpose: Fixtures reutilizáveis para os testes (OPT-16).
# Inclui um "PATH FIX" para garantir que 'src/' seja importável
# ao rodar pytest de qualquer diretório (VS Code, CI, etc.).
# ============================================================

# --- PATH FIX: coloca raiz do repo e 'src/' no sys.path ---
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]  # .../optiRota (raiz)
for p in (ROOT, ROOT / "src"):
    p = str(p)
    if p not in sys.path:
        sys.path.insert(0, p)
# ----------------------------------------------------------

import pytest
import networkx as nx

# Usamos as mesmas funções de distância do projeto,
# garantindo coerência entre pesos das arestas e heurística.
from src.utils import euclidean_distance, haversine_distance


def _add_latlon(G, n, lat, lon):
    """Helper: adiciona um nó com atributos lat/lon (para distâncias e heurísticas)."""
    G.add_node(n, lat=lat, lon=lon)


@pytest.fixture
def grid_graph_10():
    """
    Grid 2x5 (10 nós) com pesos EUCLIDIANOS.

    Por que este cenário?
    - Para testar *optimalidade* do A* vs Dijkstra num caso em que a heurística
      euclidiana é CONSISTENTE (mesma métrica dos pesos).
    - Se A* está correto e h é consistente, A* deve dar o mesmo custo que Dijkstra.

    Retorna:
      G: nx.DiGraph
      start: nó inicial (canto superior esquerdo)
      end: nó final (canto inferior direito)
    """
    G = nx.DiGraph()
    rows, cols = 2, 5
    nid = lambda r, c: r * cols + c

    # Coordenadas artificiais e espaçamento ~100 m
    lat0, lon0 = -9.6, -35.7
    dlat, dlon = 0.0009, 0.0009

    # Cria nós com lat/lon
    for r in range(rows):
        for c in range(cols):
            n = nid(r, c)
            _add_latlon(G, n, lat0 + r * dlat, lon0 + c * dlon)

    # Liga vizinhos (direita/baixo) com pesos EUCLIDIANOS (mesma métrica da heurística)
    for r in range(rows):
        for c in range(cols):
            n = nid(r, c)
            # direita
            if c + 1 < cols:
                m = nid(r, c + 1)
                w = euclidean_distance(type("N", (), G.nodes[n]), type("N", (), G.nodes[m]))
                G.add_edge(n, m, weight=w)
                G.add_edge(m, n, weight=w)  # bidirecional para simplificar
            # baixo
            if r + 1 < rows:
                m = nid(r + 1, c)
                w = euclidean_distance(type("N", (), G.nodes[n]), type("N", (), G.nodes[m]))
                G.add_edge(n, m, weight=w)
                G.add_edge(m, n, weight=w)

    start, end = nid(0, 0), nid(rows - 1, cols - 1)
    return G, start, end


@pytest.fixture
def ring_graph():
    """
    Grafo cíclico (5 nós) + 'corda' (atalho 0-2), com pesos EUCLIDIANOS.

    Por que este cenário?
    - Garante que o A* lida com CICLOS (não entra em loop).
    - Verifica se A* encontra o ATALHO quando ele reduz o custo.
    """
    G = nx.DiGraph()
    coords = [
        (-9.60,   -35.70),
        (-9.6007, -35.6993),
        (-9.6014, -35.6999),
        (-9.6009, -35.7010),
        (-9.6001, -35.7011),
    ]
    # Nós com lat/lon
    for i, (lat, lon) in enumerate(coords):
        _add_latlon(G, i, lat, lon)

    # Ciclo base
    for i in range(len(coords)):
        j = (i + 1) % len(coords)
        w = euclidean_distance(type("N", (), G.nodes[i]), type("N", (), G.nodes[j]))
        G.add_edge(i, j, weight=w)
        G.add_edge(j, i, weight=w)

    # Corda (atalho) 0-2
    w02 = euclidean_distance(type("N", (), G.nodes[0]), type("N", (), G.nodes[2]))
    G.add_edge(0, 2, weight=w02)
    G.add_edge(2, 0, weight=w02)
    return G


@pytest.fixture
def disconnected_graph():
    """
    Duas componentes desconexas (A e B), para testar destino INALCANÇÁVEL.

    Esperado no teste:
    - O A* deve sinalizar erro (exceção) ou estado 'sem caminho'.
    """
    G = nx.DiGraph()
    # componente A
    _add_latlon(G, "A1", -9.60,  -35.70)
    _add_latlon(G, "A2", -9.601, -35.699)
    # componente B
    _add_latlon(G, "B1", -9.62,  -35.72)
    _add_latlon(G, "B2", -9.621, -35.721)

    # Arestas internas em cada componente, com peso EUCLIDIANO
    for u, v in [("A1", "A2"), ("A2", "A1"), ("B1", "B2"), ("B2", "B1")]:
        w = euclidean_distance(type("N", (), G.nodes[u]), type("N", (), G.nodes[v]))
        G.add_edge(u, v, weight=w)
    return G


@pytest.fixture
def tiny_haversine_graph():
    """
    Pequeno grafo em linha (0-1-2) com pesos HAVERSINE nas arestas.

    Por que este cenário?
    - Serve para demonstrar (no teste marcado como xfail) que usar HEURÍSTICA
      EUCLIDIANA quando os PESOS são HAVERSINE pode quebrar a ADMISSIBILIDADE
      (a heurística pode superestimar).
    - Com a heurística Haversine (reta ao alvo), o A* volta a ser admissível/consistente.
    """
    G = nx.DiGraph()
    pts = {
        0: (-9.6000, -35.7000),
        1: (-9.6005, -35.7003),
        2: (-9.6010, -35.7006),
    }
    for i, (lat, lon) in pts.items():
        _add_latlon(G, i, lat, lon)

    # Peso Haversine nas arestas
    def H(u, v):
        a, b = G.nodes[u], G.nodes[v]
        return haversine_distance(a["lat"], a["lon"], b["lat"], b["lon"])

    for u, v in [(0, 1), (1, 2)]:
        G.add_edge(u, v, weight=H(u, v))
        G.add_edge(v, u, weight=H(u, v))
    return G
