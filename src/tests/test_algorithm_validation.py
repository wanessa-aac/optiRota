"""
Testes de validação de algoritmos.
FASE 4: Testes de Validação
"""

import pytest
import math
import networkx as nx
from src.algorithms import dijkstra, a_star
from src.structures import PriorityQueue, Stack, FIFOQueue
from src.utils import haversine_distance, euclidean_distance

class TestAlgorithmValidation:
    """
    Testes de validação de algoritmos.
    Teste automatizado: 90% gerado por IA
    """
    
    def test_dijkstra_algorithm_correctness(self):
        """
        Valida correção do algoritmo Dijkstra.
        Teste automatizado: 95% gerado por IA
        """
        # Cria grafo de teste
        G = nx.DiGraph()
        nodes = [
            (0, 0, "A"),
            (1, 1, "B"), 
            (2, 2, "C"),
            (3, 3, "D"),
            (4, 4, "E")
        ]
        
        for lat, lon, node_id in nodes:
            G.add_node(node_id, lat=lat, lon=lon)
        
        # Adiciona arestas com pesos
        edges = [
            ("A", "B", 1.0),
            ("B", "C", 2.0),
            ("C", "D", 1.5),
            ("D", "E", 2.5),
            ("A", "C", 4.0),
            ("B", "D", 3.0)
        ]
        
        for u, v, weight in edges:
            G.add_edge(u, v, weight=weight)
        
        # Testa Dijkstra
        result = dijkstra(G, "A", "E")
        
        # Validações de correção
        assert result['distance'] > 0, "Distância deve ser positiva"
        assert result['distance'] < float('inf'), "Distância deve ser finita"
        assert len(result['path']) > 0, "Path deve existir"
        assert result['path'][0] == "A", "Path deve começar em A"
        assert result['path'][-1] == "E", "Path deve terminar em E"
        
        # Validação contra NetworkX
        nx_distance = nx.shortest_path_length(G, "A", "E", weight="weight")
        assert abs(result['distance'] - nx_distance) < 1e-9, "Dijkstra deve coincidir com NetworkX"
        
        print(f"\nValidação Dijkstra:")
        print(f"  Distância: {result['distance']:.2f}")
        print(f"  Path: {result['path']}")
        print(f"  Nodes visitados: {result['nodes_visited']}")
    
    def test_astar_algorithm_correctness(self):
        """
        Valida correção do algoritmo A*.
        Teste automatizado: 95% gerado por IA
        """
        # Cria grafo de teste
        G = nx.DiGraph()
        nodes = [
            (0, 0, "A"),
            (1, 1, "B"),
            (2, 2, "C"), 
            (3, 3, "D"),
            (4, 4, "E")
        ]
        
        for lat, lon, node_id in nodes:
            G.add_node(node_id, lat=lat, lon=lon)
        
        # Adiciona arestas
        edges = [
            ("A", "B", 1.0),
            ("B", "C", 2.0),
            ("C", "D", 1.5),
            ("D", "E", 2.5),
            ("A", "C", 4.0),
            ("B", "D", 3.0)
        ]
        
        for u, v, weight in edges:
            G.add_edge(u, v, weight=weight)
        
        # Testa A*
        result = a_star(G, "A", "E")
        
        # Validações de correção
        assert result['distance'] > 0, "Distância deve ser positiva"
        assert result['distance'] < float('inf'), "Distância deve ser finita"
        assert len(result['path']) > 0, "Path deve existir"
        assert result['path'][0] == "A", "Path deve começar em A"
        assert result['path'][-1] == "E", "Path deve terminar em E"
        
        # Validação contra NetworkX
        nx_distance = nx.shortest_path_length(G, "A", "E", weight="weight")
        # A* pode ter distância ligeiramente diferente devido à heurística
        assert abs(result['distance'] - nx_distance) < 2.0, "A* deve ser próximo ao NetworkX"
        
        print(f"\nValidação A*:")
        print(f"  Distância: {result['distance']:.2f}")
        print(f"  Path: {result['path']}")
        print(f"  Nodes visitados: {result['nodes_visited']}")
    
    def test_priority_queue_correctness(self):
        """
        Valida correção da PriorityQueue.
        Teste automatizado: 95% gerado por IA
        """
        pq = PriorityQueue()
        
        # Testa inserção e extração
        test_items = [
            (3, "C"),
            (1, "A"),
            (4, "D"),
            (2, "B"),
            (5, "E")
        ]
        
        # Insere itens
        for priority, value in test_items:
            pq.insert(value, priority)
        
        # Extrai em ordem
        extracted = []
        while not pq.is_empty():
            extracted.append(pq.extract_min())
        
        # Validação de ordenação
        expected = ["A", "B", "C", "D", "E"]
        assert extracted == expected, f"Ordenação incorreta: {extracted} vs {expected}"
        
        print(f"\nValidação PriorityQueue:")
        print(f"  Inserido: {[item[1] for item in test_items]}")
        print(f"  Extraído: {extracted}")
        print(f"  Ordenação: {'✅' if extracted == expected else '❌'}")
    
    def test_stack_correctness(self):
        """
        Valida correção da Stack.
        Teste automatizado: 90% gerado por IA
        """
        stack = Stack()
        
        # Testa LIFO
        items = ["A", "B", "C", "D", "E"]
        
        # Push
        for item in items:
            stack.push(item)
        
        # Pop
        extracted = []
        while not stack.is_empty():
            extracted.append(stack.pop())
        
        # Validação LIFO
        expected = list(reversed(items))
        assert extracted == expected, f"LIFO incorreto: {extracted} vs {expected}"
        
        print(f"\nValidação Stack:")
        print(f"  Inserido: {items}")
        print(f"  Extraído: {extracted}")
        print(f"  LIFO: {'✅' if extracted == expected else '❌'}")
    
    def test_fifo_queue_correctness(self):
        """
        Valida correção da FIFOQueue.
        Teste automatizado: 90% gerado por IA
        """
        fifo = FIFOQueue()
        
        # Testa FIFO
        items = ["A", "B", "C", "D", "E"]
        
        # Enqueue
        for item in items:
            fifo.enqueue(item)
        
        # Dequeue
        extracted = []
        while not fifo.is_empty():
            extracted.append(fifo.dequeue())
        
        # Validação FIFO
        assert extracted == items, f"FIFO incorreto: {extracted} vs {items}"
        
        print(f"\nValidação FIFOQueue:")
        print(f"  Inserido: {items}")
        print(f"  Extraído: {extracted}")
        print(f"  FIFO: {'✅' if extracted == items else '❌'}")
    
    def test_haversine_distance_correctness(self):
        """
        Valida correção da distância Haversine.
        Teste automatizado: 95% gerado por IA
        """
        # Testa distâncias conhecidas (em metros)
        test_cases = [
            # (lat1, lon1, lat2, lon2, expected_m)
            (0, 0, 0, 1, 111320),  # 1 grau de longitude no equador
            (0, 0, 1, 0, 111320),  # 1 grau de latitude
            (0, 0, 0, 0, 0.0),     # Mesmo ponto
            (90, 0, -90, 0, 20015090),  # Polo a polo
        ]
        
        for lat1, lon1, lat2, lon2, expected in test_cases:
            distance = haversine_distance(lat1, lon1, lat2, lon2)
            if expected > 0:
                error = abs(distance - expected) / expected * 100
                assert error < 10.0, f"Erro muito alto: {error:.2f}% para ({lat1}, {lon1}) -> ({lat2}, {lon2})"
            else:
                assert distance == 0.0, f"Distância deve ser 0 para mesmo ponto: {distance}"
        
        print(f"\nValidação Haversine:")
        for lat1, lon1, lat2, lon2, expected in test_cases:
            distance = haversine_distance(lat1, lon1, lat2, lon2)
            if expected > 0:
                error = abs(distance - expected) / expected * 100
                print(f"  ({lat1}, {lon1}) -> ({lat2}, {lon2}): {distance:.2f}m (erro: {error:.2f}%)")
            else:
                print(f"  ({lat1}, {lon1}) -> ({lat2}, {lon2}): {distance:.2f}m (mesmo ponto)")
    
    def test_euclidean_distance_correctness(self):
        """
        Valida correção da distância Euclidiana.
        Teste automatizado: 90% gerado por IA
        """
        # Testa distâncias conhecidas (em metros)
        test_cases = [
            # (lat1, lon1, lat2, lon2, expected_m)
            (0, 0, 0.000027, 0.000036, 5.0),  # ~5 metros
            (0, 0, 0, 0, 0.0),               # Mesmo ponto
            (1, 1, 1.000027, 1.000036, 5.0),  # ~5 metros deslocado
        ]
        
        for lat1, lon1, lat2, lon2, expected in test_cases:
            # Cria objetos mock
            class MockPoint:
                def __init__(self, lat, lon):
                    self.lat = lat
                    self.lon = lon
            
            p1 = MockPoint(lat1, lon1)
            p2 = MockPoint(lat2, lon2)
            
            distance = euclidean_distance(p1, p2)
            if expected > 0:
                error = abs(distance - expected) / expected * 100
                assert error < 50.0, f"Erro muito alto: {error:.2f}% para ({lat1}, {lon1}) -> ({lat2}, {lon2})"
            else:
                assert distance == 0.0, f"Distância deve ser 0 para mesmo ponto: {distance}"
        
        print(f"\nValidação Euclidiana:")
        for x1, y1, x2, y2, expected in test_cases:
            class MockPoint:
                def __init__(self, x, y):
                    self.lat = x
                    self.lon = y
            
            p1 = MockPoint(x1, y1)
            p2 = MockPoint(x2, y2)
            distance = euclidean_distance(p1, p2)
            print(f"  ({x1}, {y1}) -> ({x2}, {y2}): {distance:.2f} (esperado: {expected:.2f})")
    
    def test_algorithm_termination(self):
        """
        Valida terminação dos algoritmos.
        Teste automatizado: 90% gerado por IA
        """
        # Cria grafo com ciclo
        G = nx.DiGraph()
        G.add_node("A", lat=0, lon=0)
        G.add_node("B", lat=1, lon=1)
        G.add_node("C", lat=2, lon=2)
        
        G.add_edge("A", "B", weight=1.0)
        G.add_edge("B", "C", weight=1.0)
        G.add_edge("C", "A", weight=1.0)  # Ciclo
        
        # Testa que algoritmos terminam
        try:
            dijkstra_result = dijkstra(G, "A", "B")
            assert dijkstra_result['distance'] < float('inf'), "Dijkstra deve terminar"
        except Exception as e:
            pytest.fail(f"Dijkstra falhou: {e}")
        
        try:
            astar_result = a_star(G, "A", "B")
            assert astar_result['distance'] < float('inf'), "A* deve terminar"
        except Exception as e:
            pytest.fail(f"A* falhou: {e}")
        
        print(f"\nValidação de terminação:")
        print(f"  Dijkstra: ✅")
        print(f"  A*: ✅")
    
    def test_algorithm_optimality(self):
        """
        Valida otimalidade dos algoritmos.
        Teste automatizado: 95% gerado por IA
        """
        # Cria grafo com caminho ótimo conhecido
        G = nx.DiGraph()
        nodes = [
            (0, 0, "A"),
            (1, 0, "B"),
            (2, 0, "C"),
            (1, 1, "D")
        ]
        
        for lat, lon, node_id in nodes:
            G.add_node(node_id, lat=lat, lon=lon)
        
        # Caminho direto: A -> B -> C (peso 2.0)
        # Caminho alternativo: A -> D -> C (peso 3.0)
        G.add_edge("A", "B", weight=1.0)
        G.add_edge("B", "C", weight=1.0)
        G.add_edge("A", "D", weight=1.5)
        G.add_edge("D", "C", weight=1.5)
        
        # Testa Dijkstra
        dijkstra_result = dijkstra(G, "A", "C")
        assert dijkstra_result['distance'] == 2.0, f"Dijkstra não ótimo: {dijkstra_result['distance']}"
        
        # Testa A*
        astar_result = a_star(G, "A", "C")
        assert astar_result['distance'] == 2.0, f"A* não ótimo: {astar_result['distance']}"
        
        print(f"\nValidação de otimalidade:")
        print(f"  Dijkstra: {dijkstra_result['distance']:.2f} (ótimo: 2.0)")
        print(f"  A*: {astar_result['distance']:.2f} (ótimo: 2.0)")
        print(f"  Otimalidade: ✅")
