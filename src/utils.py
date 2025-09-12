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


if __name__ == "__main__":
    # Teste: São Paulo (SP) -> Rio de Janeiro (RJ)
    sp = (-23.5505, -46.6333)
    rj = (-22.9068, -43.1729)

    distancia = haversine_distance(sp[0], sp[1], rj[0], rj[1])

    # Salva em arquivo temporário para validação
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as tmp:
        tmp.write(f"Distância SP-RJ: {distancia:.2f} km\n")
        print(f"Resultado salvo em: {tmp.name}")
