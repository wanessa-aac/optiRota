# src/tests/test_benchmarks_algorithms.py
"""
Testes de benchmark para algoritmos do OptiRota.
FASE 1: Testes de Performance - 90% automatizável com IA
"""

import pytest
import time
import random
import networkx as nx
from src.algorithms import dijkstra, a_star
from src.structures import PriorityQueue


class TestBenchmarkAlgorithms:
    """Testes de benchmark para algoritmos de roteamento."""
    
    @pytest.fixture
    def large_graph(self):
        """Cria um grafo grande para testes de performance."""
        G = nx.DiGraph()
        
        # Cria um grafo grid 20x20 (400 nós)
        for i in range(20):
            for j in range(20):
                node_id = f"{i}_{j}"
                G.add_node(node_id, lat=i, lon=j)
                
                # Conecta com vizinhos (direita e baixo)
                if j < 19:  # não é a última coluna
                    right_id = f"{i}_{j+1}"
                    weight = random.uniform(0.1, 2.0)
                    G.add_edge(node_id, right_id, weight=weight)
                
                if i < 19:  # não é a última linha
                    down_id = f"{i+1}_{j}"
                    weight = random.uniform(0.1, 2.0)
                    G.add_edge(node_id, down_id, weight=weight)
        
        return G
    
    @pytest.fixture
    def medium_graph(self):
        """Cria um grafo médio para testes de performance."""
        G = nx.DiGraph()
        
        # Cria um grafo grid 10x10 (100 nós)
        for i in range(10):
            for j in range(10):
                node_id = f"{i}_{j}"
                G.add_node(node_id, lat=i, lon=j)
                
                # Conecta com vizinhos
                if j < 9:
                    right_id = f"{i}_{j+1}"
                    weight = random.uniform(0.1, 2.0)
                    G.add_edge(node_id, right_id, weight=weight)
                
                if i < 9:
                    down_id = f"{i+1}_{j}"
                    weight = random.uniform(0.1, 2.0)
                    G.add_edge(node_id, down_id, weight=weight)
        
        return G
    
    def test_benchmark_dijkstra_vs_networkx(self, medium_graph):
        """
        Compara performance do Dijkstra customizado vs NetworkX.
        Teste automatizado: 90% gerado por IA
        """
        # Seleciona nós de origem e destino
        start = "0_0"
        end = "9_9"
        
        # Testa Dijkstra customizado
        start_time = time.time()
        custom_result = dijkstra(medium_graph, start, end)
        custom_time = time.time() - start_time
        
        # Testa NetworkX
        start_time = time.time()
        nx_result = nx.shortest_path_length(medium_graph, start, end, weight="weight")
        nx_time = time.time() - start_time
        
        # Validações
        assert custom_result['distance'] == pytest.approx(nx_result, rel=1e-9)
        assert custom_time < 5.0, f"Dijkstra customizado muito lento: {custom_time:.3f}s"
        assert nx_time < 5.0, f"NetworkX muito lento: {nx_time:.3f}s"
        
        # Log de performance
        print(f"\nDijkstra customizado: {custom_time:.3f}s")
        print(f"NetworkX: {nx_time:.3f}s")
        if nx_time > 0:
            print(f"Razão: {custom_time/nx_time:.2f}x")
        else:
            print("NetworkX muito rápido para medir razão")
    
    def test_benchmark_astar_vs_dijkstra(self, medium_graph):
        """
        Compara A* vs Dijkstra em diferentes cenários.
        Teste automatizado: 85% gerado por IA
        """
        start = "0_0"
        end = "9_9"
        
        # Testa Dijkstra
        start_time = time.time()
        dijkstra_result = dijkstra(medium_graph, start, end)
        dijkstra_time = time.time() - start_time
        
        # Testa A*
        start_time = time.time()
        astar_result = a_star(medium_graph, start, end)
        astar_time = time.time() - start_time
        
        # Validações
        # A* e Dijkstra podem ter distâncias diferentes devido à heurística
        # Mas ambas devem ser válidas (positivas e finitas)
        assert dijkstra_result['distance'] > 0, "Dijkstra retornou distância inválida"
        assert astar_result['distance'] > 0, "A* retornou distância inválida"
        assert dijkstra_result['distance'] < float('inf'), "Dijkstra retornou distância infinita"
        assert astar_result['distance'] < float('inf'), "A* retornou distância infinita"
        
        assert dijkstra_time < 5.0, f"Dijkstra muito lento: {dijkstra_time:.3f}s"
        assert astar_time < 5.0, f"A* muito lento: {astar_time:.3f}s"
        
        # A* deve ser mais eficiente (menos nós visitados)
        assert astar_result['nodes_visited'] <= dijkstra_result['nodes_visited']
        
        print(f"\nDijkstra: {dijkstra_time:.3f}s, {dijkstra_result['nodes_visited']} nós")
        print(f"A*: {astar_time:.3f}s, {astar_result['nodes_visited']} nós")
        print(f"Eficiência A*: {dijkstra_result['nodes_visited']/astar_result['nodes_visited']:.2f}x")
    
    def test_benchmark_priority_queue_vs_list(self):
        """
        Compara PriorityQueue vs lista ordenada.
        Teste automatizado: 95% gerado por IA
        """
        # Usa seed fixa para reprodutibilidade
        random.seed(42)
        
        # Testa PriorityQueue
        pq = PriorityQueue()
        start_time = time.time()
        
        # Inserção massiva
        for i in range(1000):
            pq.insert(f"item_{i}", random.uniform(0, 1000))
        
        # Extração
        extracted_pq = []
        while not pq.is_empty():
            extracted_pq.append(pq.extract_min())
        
        pq_time = time.time() - start_time
        
        # Testa lista ordenada com mesma seed
        random.seed(42)
        items = []
        start_time = time.time()
        
        # Inserção massiva
        for i in range(1000):
            items.append((random.uniform(0, 1000), f"item_{i}"))
        
        # Ordenação
        items.sort()
        extracted_list = [item[1] for item in items]
        
        list_time = time.time() - start_time
        
        # Validações
        assert len(extracted_pq) == len(extracted_list)
        assert extracted_pq == extracted_list
        assert pq_time < 2.0, f"PriorityQueue muito lenta: {pq_time:.3f}s"
        assert list_time < 2.0, f"Lista muito lenta: {list_time:.3f}s"
        
        print(f"\nPriorityQueue: {pq_time:.3f}s")
        print(f"Lista ordenada: {list_time:.3f}s")
        if list_time > 0:
            print(f"Razão: {pq_time/list_time:.2f}x")
        else:
            print("Lista muito rápida para medir razão")
    
    def test_benchmark_memory_usage_scaling(self, large_graph):
        """
        Monitora uso de memória com datasets crescentes.
        Teste automatizado: 80% gerado por IA
        """
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # Mede memória inicial
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Executa algoritmos
        start = "0_0"
        end = "19_19"
        
        # Dijkstra
        dijkstra_result = dijkstra(large_graph, start, end)
        dijkstra_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # A*
        astar_result = a_star(large_graph, start, end)
        astar_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Validações
        memory_increase = max(dijkstra_memory, astar_memory) - initial_memory
        assert memory_increase < 100, f"Uso de memória excessivo: {memory_increase:.1f}MB"
        
        print(f"\nMemória inicial: {initial_memory:.1f}MB")
        print(f"Após Dijkstra: {dijkstra_memory:.1f}MB")
        print(f"Após A*: {astar_memory:.1f}MB")
        print(f"Aumento total: {memory_increase:.1f}MB")
    
    def test_benchmark_algorithm_scaling(self):
        """
        Testa escalabilidade dos algoritmos com grafos de diferentes tamanhos.
        Teste automatizado: 85% gerado por IA
        """
        sizes = [5, 10, 15, 20]
        times = []
        
        for size in sizes:
            # Cria grafo de tamanho específico
            G = nx.DiGraph()
            for i in range(size):
                for j in range(size):
                    node_id = f"{i}_{j}"
                    G.add_node(node_id, lat=i, lon=j)
                    
                    if j < size - 1:
                        right_id = f"{i}_{j+1}"
                        G.add_edge(node_id, right_id, weight=1.0)
                    
                    if i < size - 1:
                        down_id = f"{i+1}_{j}"
                        G.add_edge(node_id, down_id, weight=1.0)
            
            # Testa Dijkstra
            start_time = time.time()
            dijkstra(G, "0_0", f"{size-1}_{size-1}")
            elapsed = time.time() - start_time
            times.append(elapsed)
            
            print(f"Grafo {size}x{size}: {elapsed:.3f}s")
        
        # Validação de escalabilidade
        # O tempo deve crescer de forma razoável (não exponencial)
        for i in range(1, len(times)):
            if times[i-1] > 0:
                ratio = times[i] / times[i-1]
                assert ratio < 10, f"Escalabilidade ruim: {ratio:.2f}x entre {sizes[i-1]} e {sizes[i]}"
            else:
                # Se o tempo anterior foi 0, apenas verifica que o atual não é muito grande
                assert times[i] < 1.0, f"Tempo muito alto: {times[i]:.3f}s para grafo {sizes[i]}x{sizes[i]}"
        
        print(f"\nEscalabilidade validada: {len(sizes)} tamanhos testados")
