import json
import networkx as nx
from src.algorithms import dijkstra, get_shortest_path_info
from src.structures import PriorityQueue, reconstruct_path

def carregar_grafo(json_path="data/graph.json"):
    """Carrega o grafo a partir de graph.json"""
    with open(json_path, "r") as f:
        data = json.load(f)

    G = nx.DiGraph()

    # Adiciona nós
    for node in data["nodes"]:
        G.add_node(node["id"], lat=node["lat"], lon=node["lon"])

    # Adiciona arestas
    for edge in data["links"]:
        G.add_edge(
            edge["source"],
            edge["target"],
            weight=edge.get("weight", 1.0),
            highway=edge.get("highway")
        )
    return G

if __name__ == "__main__":
    # 1. Carrega o grafo
    grafo = carregar_grafo()

    # 2. Pergunta IDs de start e end via terminal
    start = int(input("Digite o ID do nó de origem: "))
    end = int(input("Digite o ID do nó de destino: "))

    # 3. Executa Dijkstra
    try:
        resultado = dijkstra(grafo, start, end)
        print(get_shortest_path_info(resultado))
    except RuntimeError as e:
        print("⚠️", e)
    except ValueError as e:
        print("❌", e)
