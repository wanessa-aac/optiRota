# src/parser_osm.py
import os
import logging
import osmnx as ox

# Configuração de logs
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/parser.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def parse_osm(file_path: str):
    """
    Faz parsing de um arquivo .osm/.xml local e retorna nodes significativos e ways.
    
    Retorna:
        dict com {'nodes': {id: {...}}, 'ways': [{from, to, highway, oneway, length}]}
    """
    if not os.path.exists(file_path):
        logging.error("Arquivo não encontrado: %s", file_path)
        raise FileNotFoundError(file_path)

    logging.info("Iniciando parsing de %s", file_path)

    # Carrega o grafo com osmnx
    G = ox.graph_from_xml(file_path, simplify=False, retain_all=True)

    # Extrair nodes
    nodes = {}
    for nid, data in G.nodes(data=True):
        lon = data.get("x") or data.get("lon")
        lat = data.get("y") or data.get("lat")
        nodes[nid] = {"lat": lat, "lon": lon}

    # Extrair ways (arestas)
    ways = []
    for u, v, k, data in G.edges(keys=True, data=True):
        ways.append({
            "from": u,
            "to": v,
            "highway": data.get("highway"),
            "oneway": data.get("oneway"),
            "length": data.get("length"),
            "tags": {k: v for k, v in data.items()}  # mantém todas as tags
        })

    # Filtrar nodes: grau != 2 (interseções e extremidades)
    significant_nodes = {
        nid: info for nid, info in nodes.items()
        if G.degree(nid) != 2
    }

    logging.info("Nodes totais: %d | Nodes significativos: %d", len(nodes), len(significant_nodes))
    logging.info("Ways totais: %d", len(ways))

    return {"nodes": significant_nodes, "ways": ways}


if __name__ == "__main__":
    file = "data/maceio_ponta_verde.osm"  # ajuste se necessário
    try:
        data = parse_osm(file)
        print(f"Parser finalizado. {len(data['nodes'])} nodes significativos e {len(data['ways'])} ways processados.")
    except Exception as e:
        print(f"Erro: {e}")
        logging.exception("Erro no parse")
