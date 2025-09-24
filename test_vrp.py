import networkx as nx
from src.algorithms import vrp_solver

def main():
    # Criar grafo completo (distância unitária)
    G = nx.complete_graph(4)
    for u, v in G.edges:
        G[u][v]["weight"] = 1

    # Definir pedidos
    orders = [
        {"id": 1, "node": 1, "weight": 30, "time": 10},
        {"id": 2, "node": 2, "weight": 50, "time": 10},
        {"id": 3, "node": 3, "weight": 40, "time": 12},  # fora da janela
    ]

    # Executar solver
    rota = vrp_solver(G, orders)
    print("Rota encontrada:", rota)

if __name__ == "__main__":
    main()
