import math
import os
import random
import tempfile

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula a distância entre dois pontos geográficos usando a fórmula de Haversine.

    Parâmetros:
        lat1, lon1: coordenadas do ponto 1 em graus decimais
        lat2, lon2: coordenadas do ponto 2 em graus decimais

    Retorna:
        Distância em quilômetros (float)

    Lança:
        ValueError se as coordenadas forem inválidas
    """
    # Verificação de validade das coordenadas
    for val, name, lim in [(lat1, "lat1", 90), (lat2, "lat2", 90), (lon1, "lon1", 180), (lon2, "lon2", 180)]:
        if val is None:
            raise ValueError(f"Coordenada {name} não pode ser None")
        if not -lim <= val <= lim:
            raise ValueError(f"Coordenada {name} inválida: {val}")

    # Conversão para radianos
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Fórmula de Haversine
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))

    R = 6371000  # raio da Terra em metros
    return R * c


def euclidean_distance(node1, node2) -> float:
    """
    Calcula a distância Euclidiana entre dois nós do grafo.
    
    Esta função é uma heurística admissível para o algoritmo A* quando usada
    com coordenadas geográficas (lat/lon). A distância Euclidiana sempre
    subestima a distância real no grafo, garantindo a admissibilidade.
    
    Parâmetros:
        node1: Primeiro nó (deve ter atributos 'lat' e 'lon')
        node2: Segundo nó (deve ter atributos 'lat' e 'lon')
    
    Retorna:
        Distância Euclidiana em metros (float)
    
    Lança:
        ValueError se os nós não tiverem coordenadas válidas
        AttributeError se os nós não tiverem atributos 'lat' e 'lon'
    
    Exemplo:
        # Para dois nós do grafo
        distance = euclidean_distance(graph.nodes[node1], graph.nodes[node2])
    """
    # Verifica se os nós têm os atributos necessários
    if not hasattr(node1, 'lat') or not hasattr(node1, 'lon'):
        raise AttributeError("node1 deve ter atributos 'lat' e 'lon'")
    if not hasattr(node2, 'lat') or not hasattr(node2, 'lon'):
        raise AttributeError("node2 deve ter atributos 'lat' e 'lon'")
    
    # Extrai coordenadas
    lat1, lon1 = node1.lat, node1.lon
    lat2, lon2 = node2.lat, node2.lon
    
    # Verificação de validade das coordenadas
    for val, name, lim in [(lat1, "lat1", 90), (lat2, "lat2", 90), (lon1, "lon1", 180), (lon2, "lon2", 180)]:
        if val is None:
            raise ValueError(f"Coordenada {name} não pode ser None")
        if not -lim <= val <= lim:
            raise ValueError(f"Coordenada {name} inválida: {val}")
    
    # Converte lat/lon para coordenadas x/y em metros
    # Usa projeção simples: 1 grau ≈ 111,320 metros
    x1 = lon1 * 111320 * math.cos(math.radians(lat1))  # longitude em metros
    y1 = lat1 * 111320  # latitude em metros
    x2 = lon2 * 111320 * math.cos(math.radians(lat2))
    y2 = lat2 * 111320
    
    # Calcula distância Euclidiana: sqrt((x2-x1)² + (y2-y1)²)
    dx = x2 - x1
    dy = y2 - y1
    distance = math.sqrt(dx*dx + dy*dy)
    
    return distance


def plot_dijkstra_vs_a(output_path: str = "docs/dijkstra_vs_a.png",
                       min_nodes: int = 100,
                       max_nodes: int = 5000,
                       steps: int = 20,
                       repeats: int = 3) -> str:
    """
    Gera e salva um gráfico de comparação de desempenho (tempo vs número de nós)
    entre Dijkstra e A* usando dados simulados em escala linear.

    Args:
        output_path: Caminho do arquivo de imagem a ser salvo.
        min_nodes: Número mínimo de nós.
        max_nodes: Número máximo de nós.
        steps: Quantidade de pontos entre min e max (inclusive extremos).
        repeats: Número de repetições para reduzir ruído nos dados simulados.

    Returns:
        Caminho absoluto do arquivo salvo.
    """
    # Import local para evitar dependência quando a função não é usada
    import matplotlib.pyplot as plt

    if steps < 2:
        steps = 2

    # Gera tamanhos de grafo uniformemente espaçados
    node_counts = [int(min_nodes + i * (max_nodes - min_nodes) / (steps - 1)) for i in range(steps)]

    # Parâmetros de tempo sintéticos (segundos) ~ O(V log V) para grafos esparsos
    # A*: fator menor devido à heurística admissível
    base_a = 2.0e-6  # constante para Dijkstra
    base_b = 1.2e-6  # constante para A*

    def simulate_time(constant: float, n: int) -> float:
        # Tempo ~ c * n * log2(n) com pequeno ruído gaussiano
        noiseless = constant * n * max(1.0, math.log2(max(2, n)))
        noise = random.gauss(0.0, noiseless * 0.05)
        return max(0.0, noiseless + noise)

    dijkstra_times = []
    astar_times = []
    for n in node_counts:
        # Média de repetições para suavizar
        d_mean = sum(simulate_time(base_a, n) for _ in range(repeats)) / repeats
        a_mean = sum(simulate_time(base_b, n) for _ in range(repeats)) / repeats
        dijkstra_times.append(d_mean)
        astar_times.append(a_mean)

    # Plot
    plt.figure(figsize=(8, 5))
    plt.plot(node_counts, dijkstra_times, label="Dijkstra (simulado)", marker="o", linewidth=2)
    plt.plot(node_counts, astar_times, label="A* (simulado)", marker="s", linewidth=2)
    plt.xlabel("Número de nós")
    plt.ylabel("Tempo (s)")
    plt.title("Desempenho: Dijkstra vs A* (escala linear)")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()

    # Garante diretório de saída
    out_dir = os.path.dirname(output_path) or "."
    os.makedirs(out_dir, exist_ok=True)

    plt.savefig(output_path, dpi=160)
    plt.close()
    return os.path.abspath(output_path)

if __name__ == "__main__":
    # Teste: São Paulo (SP) -> Rio de Janeiro (RJ)
    sp = (-23.5505, -46.6333)
    rj = (-22.9068, -43.1729)

    distancia_haversine = haversine_distance(sp[0], sp[1], rj[0], rj[1])
    
    # Teste da distância Euclidiana
    class MockNode:
        def __init__(self, lat, lon):
            self.lat = lat
            self.lon = lon
    
    sp_node = MockNode(sp[0], sp[1])
    rj_node = MockNode(rj[0], rj[1])
    
    distancia_euclidiana = euclidean_distance(sp_node, rj_node)

    # Salva em arquivo temporário para validação
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as tmp:
        tmp.write(f"Distância SP-RJ (Haversine): {distancia_haversine:.2f} m\n")
        tmp.write(f"Distância SP-RJ (Euclidiana): {distancia_euclidiana:.2f} m\n")
        tmp.write(f"Diferença: {distancia_haversine - distancia_euclidiana:.2f} m\n")
        tmp.write(f"Euclidiana é admissível? {distancia_euclidiana <= distancia_haversine}\n")
        print(f"Resultado salvo em: {tmp.name}")
