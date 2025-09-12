# src/graph.py

import os
import json
import logging
import networkx as nx
from networkx.readwrite import json_graph

from .utils import haversine_distance
from .parser_osm import parse_osm  # Import correto do parser local

# Configuração de logs
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/parser.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def simplify_degree2_directed(G: nx.DiGraph) -> nx.DiGraph:
    """
    Contrai nós 'intermediários' cujo conjunto de vizinhos (preds ∪ succs) tem exatamente 2 nós.
    Preserva direção: se existir a->n e n->b, cria/atualiza a->b com peso somado; idem b->n->a.
    Remove n. Repete até não haver mais contrações.
    """
    H = G.copy()
    changed = True
    while changed:
        changed = False
        # usamos a visão não-direcionada para detectar grau-2 "topológico"
        UG = H.to_undirected()
        # lista para evitar modificar iterável enquanto removemos nós
        candidates = [n for n, d in UG.degree() if d == 2]
        for n in candidates:
            if n not in H:  # já pode ter sido removido
                continue
            preds = set(H.predecessors(n))
            succs = set(H.successors(n))
            neighbors = preds | succs
            if len(neighbors) != 2:
                continue
            a, b = tuple(neighbors)

            # direção a->n->b
            if H.has_edge(a, n) and H.has_edge(n, b):
                w = H[a][n]['weight'] + H[n][b]['weight']
                if H.has_edge(a, b):
                    H[a][b]['weight'] = min(H[a][b]['weight'], w)
                else:
                    H.add_edge(a, b, weight=w)

            # direção b->n->a
            if H.has_edge(b, n) and H.has_edge(n, a):
                w = H[b][n]['weight'] + H[n][a]['weight']
                if H.has_edge(b, a):
                    H[b][a]['weight'] = min(H[b][a]['weight'], w)
                else:
                    H.add_edge(b, a, weight=w)

            # remover o nó intermediário
            # (após criar as arestas diretas necessárias)
            H.remove_node(n)
            changed = True
    return H


def build_graph(parsed_data):
    """
    Constrói um grafo direcionado a partir dos dados parseados.
    Cada aresta recebe o peso calculado pela distância Haversine.
    """
    G = nx.DiGraph()

    # Adiciona nós (cruzamentos)
    for node_id, data in parsed_data["nodes"].items():
        G.add_node(node_id, **data)

    # Adiciona arestas com pesos
    for way in parsed_data["ways"]:
        tags = way.get("tags", {})

        # Filtros de tags
        if tags.get("access") == "private":
            continue

        oneway = tags.get("oneway") == "yes"
        u, v = way["from"], way["to"]

        # Confere se ambos os nós existem
        if u not in parsed_data["nodes"] or v not in parsed_data["nodes"]:
            continue

        lat1, lon1 = parsed_data["nodes"][u]["lat"], parsed_data["nodes"][u]["lon"]
        lat2, lon2 = parsed_data["nodes"][v]["lat"], parsed_data["nodes"][v]["lon"]

        # Calcula distância Haversine
        dist = haversine_distance(lat1, lon1, lat2, lon2)

        # Adiciona aresta u -> v
        G.add_edge(u, v, weight=dist, highway=tags.get("highway"))

        # Se não for oneway, adiciona v -> u
        if not oneway:
            G.add_edge(v, u, weight=dist, highway=tags.get("highway"))

         # Simplifica o grafo removendo nós intermediários de grau 2
        try:
            import osmnx as ox
            G = ox.utils_graph.simplify_graph(G)
        except Exception as e:
            import logging
            logging.info(f"Não foi possível simplificar com osmnx: {e}")

        # 1) simplificação manual de nós grau-2
        G = simplify_degree2_directed(G)

        # 2) manter só o maior componente fracamente conexo (remove isolados)
        if G.number_of_nodes() > 0:
            wccs = list(nx.weakly_connected_components(G))
            giant = max(wccs, key=len)
            G = G.subgraph(giant).copy()



    return G


if __name__ == "__main__":
    osm_file = "data/090925maceio_ponta_verde.osm"  # arquivo de entrada
    if not os.path.exists(osm_file):
        raise FileNotFoundError(f"Arquivo OSM não encontrado: {osm_file}")

    # Parse do OSM
    parsed = parse_osm(osm_file)

    # Cria o grafo
    G = build_graph(parsed)

    # Verifica conectividade
    strongly_connected = nx.is_strongly_connected(G)
    logging.info(f"Grafo fortemente conexo? {strongly_connected}")

    # Exporta grafo como JSON
    os.makedirs("data", exist_ok=True)
    graph_json = json_graph.node_link_data(G)
    with open("data/graph.json", "w", encoding="utf-8") as f:
        json.dump(graph_json, f, ensure_ascii=False, indent=2)

    logging.info(f"Grafo salvo em data/graph.json com {len(G.nodes)} nós e {len(G.edges)} arestas")
    print("✅ Grafo gerado e exportado em data/graph.json")
