# src/graph.py
import os
import logging
import osmnx as ox

# logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/parser.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def parse_place(place_name: str, network_type: str = "drive"):
    """
    Faz o parsing de uma região via Overpass API e retorna nodes e ways.
    - place_name: nome do bairro/cidade (ex: "Ponta Verde, Maceió, Brasil")
    - network_type: 'drive', 'walk', 'bike', etc.
    """
    logging.info("Iniciando parsing de %s", place_name)

    # baixa grafo direto do OSM (Overpass)
    G = ox.graph_from_place(place_name, network_type=network_type, simplify=False)

    # extrair nodes
    nodes = {
        nid: {"lat": data.get("y"), "lon": data.get("x")}
        for nid, data in G.nodes(data=True)
    }

    # extrair ways
    ways = []
    for u, v, k, data in G.edges(keys=True, data=True):
        ways.append({
            "from": u,
            "to": v,
            "highway": data.get("highway"),
            "oneway": data.get("oneway"),
            "length": data.get("length"),
        })

    # filtrar nodes significativos (interseções e dead-ends)
    significant_nodes = {
        nid: info for nid, info in nodes.items()
        if G.degree(nid) != 2
    }

    logging.info("Nodes totais: %d | Nodes significativos: %d", len(nodes), len(significant_nodes))
    logging.info("Ways totais: %d", len(ways))

    return {"nodes": significant_nodes, "ways": ways}

if __name__ == "__main__":
    place = "Ponta Verde, Maceió, Brasil"
    try:
        data = parse_place(place)
        print(f"Parser finalizado. {len(data['nodes'])} nodes significativos e {len(data['ways'])} ways processados.")
    except Exception as e:
        print(f"Erro: {e}")
        logging.exception("Erro no parse")
