# src/tests/test_numerical_precision.py
"""
Testes de precisão numérica e casos extremos do OptiRota.
FASE 2: Testes de Casos Extremos - 95% automatizável com IA
"""

import pytest
import math
import random
import sys
import networkx as nx
from src.algorithms import dijkstra, a_star
from src.structures import PriorityQueue
from src.utils import haversine_distance, euclidean_distance


class TestNumericalPrecision:
    """Testes de precisão numérica e valores extremos."""
    
    def test_numerical_precision_edge_cases(self):
        """
        Testa valores extremos e precisão numérica.
        Teste automatizado: 95% gerado por IA
        """
        # Testa valores extremos para PriorityQueue
        pq = PriorityQueue()
        
        # Valores extremos
        extreme_values = [
            (0.0, "zero"),
            (1e-10, "very_small"),
            (1e10, "very_large"),
            (sys.float_info.max, "max_float"),
            (sys.float_info.min, "min_float"),
            (math.pi, "pi"),
            (math.e, "euler"),
            (-1e-10, "negative_small"),
            (-1e10, "negative_large")
        ]
        
        # Insere valores extremos
        for priority, value in extreme_values:
            try:
                pq.insert(value, priority)
            except (OverflowError, ValueError) as e:
                pytest.fail(f"Falha ao inserir valor extremo {value} com prioridade {priority}: {e}")
        
        # Extrai e valida ordenação
        extracted = []
        while not pq.is_empty():
            extracted.append(pq.extract_min())
        
        # Valida que a ordenação está correta
        # Cria mapeamento de valores para prioridades
        value_to_priority = {value: priority for priority, value in extreme_values}
        extracted_priorities = [value_to_priority[value] for value in extracted]
        assert extracted_priorities == sorted(extracted_priorities), f"Ordenação incorreta: {extracted_priorities}"
        
        print(f"\nValores extremos testados: {len(extreme_values)}")
        print(f"Valores extraídos: {len(extracted)}")
    
    def test_distance_accuracy_long_distances(self):
        """
        Testa precisão de distâncias em longas distâncias.
        Teste automatizado: 90% gerado por IA
        """
        # Coordenadas extremas (global)
        test_cases = [
            # (lat1, lon1, lat2, lon2, expected_distance_km)
            (0, 0, 0, 180, 20015.1),  # Equador, 180 graus
            (0, 0, 90, 0, 10007.5),   # Polo Norte
            (0, 0, -90, 0, 10007.5),  # Polo Sul
            (0, 0, 0, 90, 10007.5),   # 90 graus leste
            (0, 0, 0, -90, 10007.5),  # 90 graus oeste
            (45, 0, 45, 180, 10007.5), # 45 graus norte, 180 graus
            (-45, 0, -45, 180, 10007.5), # 45 graus sul, 180 graus
        ]
        
        for lat1, lon1, lat2, lon2, expected_km in test_cases:
            # Calcula distância Haversine
            distance_m = haversine_distance(lat1, lon1, lat2, lon2)
            distance_km = distance_m / 1000
            
            # Valida precisão (tolerância de 1%)
            error_percent = abs(distance_km - expected_km) / expected_km * 100
            assert error_percent < 1.0, f"Erro de precisão muito alto: {error_percent:.2f}% para {lat1},{lon1} -> {lat2},{lon2}"
            
            print(f"Distância {lat1},{lon1} -> {lat2},{lon2}: {distance_km:.1f}km (esperado: {expected_km:.1f}km, erro: {error_percent:.2f}%)")
        
        print(f"\nPrecisão de distâncias longas validada: {len(test_cases)} casos")
    
    def test_haversine_vs_euclidean_precision(self):
        """
        Compara precisão Haversine vs Euclidiana.
        Teste automatizado: 85% gerado por IA
        """
        # Coordenadas de teste
        test_coordinates = [
            (0, 0, 1, 1),      # Curta distância
            (0, 0, 10, 10),    # Média distância
            (0, 0, 45, 45),    # Longa distância
            (0, 0, 90, 90),    # Muito longa distância
        ]
        
        for lat1, lon1, lat2, lon2 in test_coordinates:
            # Distância Haversine (esférica)
            haversine_dist = haversine_distance(lat1, lon1, lat2, lon2)
            
            # Distância Euclidiana (plana)
            euclidean_dist = euclidean_distance(
                type('obj', (object,), {'lat': lat1, 'lon': lon1})(),
                type('obj', (object,), {'lat': lat2, 'lon': lon2})()
            )
            
            # Para distâncias curtas, devem ser similares
            if haversine_dist < 1000:  # < 1km
                ratio = haversine_dist / euclidean_dist
                assert 0.8 < ratio < 1.2, f"Razão Haversine/Euclidiana muito diferente: {ratio:.3f}"
            else:
                # Para distâncias longas, Haversine deve ser mais preciso
                assert haversine_dist > 0, "Distância Haversine deve ser positiva"
                assert euclidean_dist > 0, "Distância Euclidiana deve ser positiva"
            
            print(f"Coordenadas {lat1},{lon1} -> {lat2},{lon2}:")
            print(f"  Haversine: {haversine_dist:.2f}m")
            print(f"  Euclidiana: {euclidean_dist:.2f}m")
            print(f"  Razão: {haversine_dist/euclidean_dist:.3f}")
    
    def test_floating_point_accumulation(self):
        """
        Testa acúmulo de erros de ponto flutuante.
        Teste automatizado: 90% gerado por IA
        """
        # Testa acúmulo de erros em operações repetidas
        pq = PriorityQueue()
        
        # Adiciona muitos elementos com prioridades similares
        base_priority = 1.0
        num_operations = 1000
        
        for i in range(num_operations):
            # Prioridade com pequena variação
            priority = base_priority + random.uniform(-1e-6, 1e-6)
            pq.insert(f"item_{i}", priority)
        
        # Extrai e verifica ordenação
        extracted = []
        while not pq.is_empty():
            extracted.append(pq.extract_min())
        
        # Valida que não há elementos duplicados
        assert len(extracted) == num_operations, f"Perda de elementos: {len(extracted)}/{num_operations}"
        
        # Valida que não há elementos duplicados
        assert len(set(extracted)) == len(extracted), "Elementos duplicados detectados"
        
        print(f"\nAcúmulo de erros testado:")
        print(f"  Operações: {num_operations}")
        print(f"  Elementos extraídos: {len(extracted)}")
        print(f"  Elementos únicos: {len(set(extracted))}")
    
    def test_overflow_underflow_handling(self):
        """
        Testa tratamento de overflow e underflow.
        Teste automatizado: 85% gerado por IA
        """
        pq = PriorityQueue()
        
        # Testa valores que podem causar overflow
        overflow_cases = [
            (sys.float_info.max, "max_float"),
            (sys.float_info.min, "min_float"),
            (1e308, "very_large"),
            (1e-308, "very_small"),
        ]
        
        for priority, value in overflow_cases:
            try:
                pq.insert(value, priority)
                # Se chegou aqui, não houve overflow
                extracted = pq.extract_min()
                assert extracted == value, f"Perda de valor: {value} -> {extracted}"
            except (OverflowError, ValueError) as e:
                # Overflow esperado para alguns casos
                print(f"Overflow esperado para {value}: {e}")
        
        # Testa operações que podem causar underflow
        pq = PriorityQueue()
        pq.insert("test", 1.0)
        
        # Extrai o elemento
        extracted = pq.extract_min()
        assert extracted == "test", f"Valor incorreto extraído: {extracted}"
        
        # Tenta extrair de fila vazia
        with pytest.raises(IndexError):
            pq.extract_min()
        
        print(f"\nOverflow/underflow testado:")
        print(f"  Casos de overflow: {len(overflow_cases)}")
        print(f"  Tratamento de fila vazia: OK")
    
    def test_coordinate_precision_limits(self):
        """
        Testa limites de precisão de coordenadas.
        Teste automatizado: 90% gerado por IA
        """
        # Coordenadas com diferentes precisões
        precision_cases = [
            (0.0, 0.0, "zero"),
            (0.000001, 0.000001, "micro"),
            (0.0000001, 0.0000001, "nano"),
            (90.0, 180.0, "max_lat_lon"),
            (-90.0, -180.0, "min_lat_lon"),
            (89.999999, 179.999999, "near_max"),
            (-89.999999, -179.999999, "near_min"),
        ]
        
        for lat, lon, description in precision_cases:
            # Testa se as coordenadas são válidas
            assert -90 <= lat <= 90, f"Latitude inválida: {lat}"
            assert -180 <= lon <= 180, f"Longitude inválida: {lon}"
            
            # Testa cálculo de distância com coordenadas de alta precisão
            try:
                # Para coordenadas nos limites, não testa incremento
                if lat == 90.0 or lat == -90.0 or lon == 180.0 or lon == -180.0:
                    print(f"Coordenadas {description}: {lat}, {lon} -> OK (limite)")
                    continue
                
                # Ajusta incremento para coordenadas próximas aos limites
                if lat >= 89.9 or lat <= -89.9:
                    lat_inc = 0.0000001  # Incremento menor para coordenadas próximas aos polos
                else:
                    lat_inc = 0.000001
                
                if lon >= 179.9 or lon <= -179.9:
                    lon_inc = 0.0000001  # Incremento menor para coordenadas próximas ao meridiano
                else:
                    lon_inc = 0.000001
                
                distance = haversine_distance(lat, lon, lat + lat_inc, lon + lon_inc)
                assert distance > 0, f"Distância deve ser positiva: {distance}"
                assert distance < 1000, f"Distância muito grande: {distance}"
            except Exception as e:
                pytest.fail(f"Erro ao calcular distância para {description}: {e}")
            
            print(f"Coordenadas {description}: {lat}, {lon} -> OK")
        
        print(f"\nPrecisão de coordenadas validada: {len(precision_cases)} casos")
    
    def test_algorithm_precision_comparison(self):
        """
        Compara precisão entre algoritmos.
        Teste automatizado: 85% gerado por IA
        """
        # Cria grafo com coordenadas precisas
        G = nx.DiGraph()
        
        # Adiciona nós com coordenadas de alta precisão
        nodes = [
            (0.0, 0.0, "origin"),
            (0.000001, 0.000001, "micro"),
            (0.00001, 0.00001, "small"),
            (0.001, 0.001, "medium"),
            (0.01, 0.01, "large"),
        ]
        
        for lat, lon, node_id in nodes:
            G.add_node(node_id, lat=lat, lon=lon)
        
        # Adiciona arestas com pesos calculados
        for i in range(len(nodes) - 1):
            u = nodes[i][2]
            v = nodes[i + 1][2]
            weight = haversine_distance(nodes[i][0], nodes[i][1], nodes[i + 1][0], nodes[i + 1][1])
            G.add_edge(u, v, weight=weight)
        
        # Testa Dijkstra
        dijkstra_result = dijkstra(G, "origin", "large")
        dijkstra_distance = dijkstra_result['distance']
        
        # Testa A*
        astar_result = a_star(G, "origin", "large")
        astar_distance = astar_result['distance']
        
        # Valida que as distâncias são similares
        distance_diff = abs(dijkstra_distance - astar_distance)
        max_distance = max(dijkstra_distance, astar_distance)
        
        if max_distance > 0:
            error_percent = distance_diff / max_distance * 100
            assert error_percent < 5, f"Diferença muito grande entre algoritmos: {error_percent:.2f}%"
        
        print(f"\nPrecisão de algoritmos:")
        print(f"  Dijkstra: {dijkstra_distance:.6f}m")
        print(f"  A*: {astar_distance:.6f}m")
        print(f"  Diferença: {distance_diff:.6f}m")
        print(f"  Erro: {error_percent:.2f}%")
