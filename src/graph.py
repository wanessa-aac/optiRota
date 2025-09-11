# src/graph.py

import os
import json
import logging
import networkx as nx
from networkx.readwrite import json_graph

from utils import haversine_distance
from parser_osm import parse_osm  # Import correto do parser local

# Configuração de logs
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/parser.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
