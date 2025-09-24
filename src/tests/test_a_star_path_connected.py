import pytest
from src.algorithms import a_star
from src.tools.run_precompute import load_graph

def test_path_exists():
    """Verifica se A* encontra caminho entre dois nós conectados."""
    G = load_graph("data/graph.json")

    # tenta achar um par conectado de verdade
    for u in G.nodes:
        neighbors = list(G.neighbors(u))
        if neighbors:  # achou pelo menos um vizinho
            v = neighbors[0]
            res = a_star(G, u, v, max_iterations=10000)
            assert res["distance"] > 0
            assert len(res["path"]) >= 2
            return

    # se nenhum nó tiver vizinho, pula o teste
    pytest.skip("Nenhum par conectado encontrado no grafo")

def test_no_path():
    """Verifica se A* falha quando o destino não existe."""
    G = load_graph("data/graph.json")
    u = list(G.nodes)[0]
    v = "999999999999"  # nó inexistente
    with pytest.raises(Exception):
        a_star(G, u, v, max_iterations=10000)