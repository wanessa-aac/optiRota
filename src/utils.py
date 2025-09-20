import math
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
