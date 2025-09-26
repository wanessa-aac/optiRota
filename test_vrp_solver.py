import networkx as nx
from src.algorithms import vrp_solver

# Função auxiliar para simular o precompute_distances
def precompute_distances(graph, nodes):
    dist = {u: {} for u in nodes}
    for u in nodes:
        for v in nodes:
            if u == v:
                dist[u][v] = 0
            else:
                dist[u][v] = nx.astar_path_length(graph, u, v, weight="weight")
    return dist

def main():
    # -----------------------------
    # 1. Criar grafo de exemplo
    # -----------------------------
    G = nx.DiGraph()
    edges = [
        (0, 1, 2), (1, 0, 2),
        (0, 2, 4), (2, 0, 4),
        (1, 2, 1), (2, 1, 1),
        (1, 3, 7), (3, 1, 7),
        (2, 3, 3), (3, 2, 3),
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    # -----------------------------
    # 2. Definir pedidos
    # -----------------------------
    orders = [
        {"id": 1, "node": 1, "weight": 20, "time_window": (9, 10)},
        {"id": 2, "node": 2, "weight": 30, "time_window": (9, 11)},
        {"id": 3, "node": 3, "weight": 40, "time_window": (10, 11)},
    ]

    # -----------------------------
    # 3. Rodar solver
    # -----------------------------
    nodes = [0] + [o["node"] for o in orders]
    dist_matrix = precompute_distances(G, nodes)

    result = vrp_solver(
        graph=G,
        orders=orders,
        capacity=50,
        time_window=(9, 11),
        distance_matrix=dist_matrix,
        depot_node=0
    )

    # -----------------------------
    # 4. Mostrar resultados
    # -----------------------------
    print("\n=== Resultado do VRP Solver ===")
    print("Rotas:", result["routes"])
    print("Distância total:", result["total_distance"])
    print("Número de veículos:", result["num_vehicles"])
    print("Pedidos não atendidos:", [o["id"] for o in result["unrouted_orders"]])
    print("Detalhes das rotas:")
    for detail in result["route_details"]:
        print("  -", detail)

if __name__ == "__main__":
    main()
