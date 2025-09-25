# src/tests/test_performance_scaling.py
"""
Testes de escalabilidade e performance do OptiRota.
FASE 1: Testes de Performance - 85% automatizável com IA
"""

import pytest
import time
import random
import networkx as nx
import os
import psutil
from src.algorithms import dijkstra, a_star, precompute_distances
from src.structures import PriorityQueue


class TestPerformanceScaling:
    """Testes de escalabilidade e performance."""
    
    @pytest.fixture
    def scaling_graphs(self):
        """Cria grafos de diferentes tamanhos para testes de escalabilidade."""
        graphs = {}
        
        for size in [5, 10, 15, 20]:
            G = nx.DiGraph()
            for i in range(size):
                for j in range(size):
                    node_id = f"{i}_{j}"
                    G.add_node(node_id, lat=i, lon=j)
                    
                    # Conecta com vizinhos
                    if j < size - 1:
                        right_id = f"{i}_{j+1}"
                        weight = random.uniform(0.1, 2.0)
                        G.add_edge(node_id, right_id, weight=weight)
                    
                    if i < size - 1:
                        down_id = f"{i+1}_{j}"
                        weight = random.uniform(0.1, 2.0)
                        G.add_edge(node_id, down_id, weight=weight)
            
            graphs[size] = G
        
        return graphs
    
    def test_performance_degradation_graceful(self, scaling_graphs):
        """
        Testa degradação gradual de performance.
        Teste automatizado: 90% gerado por IA
        """
        results = []
        
        for size, G in scaling_graphs.items():
            start = "0_0"
            end = f"{size-1}_{size-1}"
            
            # Testa Dijkstra
            start_time = time.time()
            dijkstra_result = dijkstra(G, start, end)
            dijkstra_time = time.time() - start_time
            
            # Testa A*
            start_time = time.time()
            astar_result = a_star(G, start, end)
            astar_time = time.time() - start_time
            
            results.append({
                'size': size,
                'nodes': G.number_of_nodes(),
                'edges': G.number_of_edges(),
                'dijkstra_time': dijkstra_time,
                'astar_time': astar_time,
                'dijkstra_nodes': dijkstra_result['nodes_visited'],
                'astar_nodes': astar_result['nodes_visited']
            })
            
            print(f"Grafo {size}x{size}: Dijkstra={dijkstra_time:.3f}s, A*={astar_time:.3f}s")
        
        # Validação de degradação gradual
        for i in range(1, len(results)):
            prev = results[i-1]
            curr = results[i]
            
            # Tempo deve crescer de forma razoável
            if prev['dijkstra_time'] > 0:
                dijkstra_ratio = curr['dijkstra_time'] / prev['dijkstra_time']
                assert dijkstra_ratio < 20, f"Dijkstra degradação excessiva: {dijkstra_ratio:.2f}x"
            else:
                # Se o tempo anterior foi 0, apenas verifica que o atual não é muito grande
                assert curr['dijkstra_time'] < 1.0, f"Dijkstra muito lento: {curr['dijkstra_time']:.3f}s"
            
            if prev['astar_time'] > 0:
                astar_ratio = curr['astar_time'] / prev['astar_time']
                assert astar_ratio < 20, f"A* degradação excessiva: {astar_ratio:.2f}x"
            else:
                # Se o tempo anterior foi 0, apenas verifica que o atual não é muito grande
                assert curr['astar_time'] < 1.0, f"A* muito lento: {curr['astar_time']:.3f}s"
        
        print(f"\nDegradação gradual validada: {len(results)} tamanhos testados")
    
    def test_large_dataset_memory_constraints(self, scaling_graphs):
        """
        Testa limites de memória com datasets grandes.
        Teste automatizado: 85% gerado por IA
        """
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        memory_usage = []
        
        for size, G in scaling_graphs.items():
            # Mede memória antes
            before_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Executa algoritmo
            start = "0_0"
            end = f"{size-1}_{size-1}"
            dijkstra(G, start, end)
            
            # Mede memória depois
            after_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = after_memory - before_memory
            
            memory_usage.append({
                'size': size,
                'nodes': G.number_of_nodes(),
                'memory_increase': memory_increase,
                'total_memory': after_memory
            })
            
            print(f"Grafo {size}x{size}: +{memory_increase:.1f}MB (total: {after_memory:.1f}MB)")
        
        # Validação de limites de memória
        max_memory = max(usage['total_memory'] for usage in memory_usage)
        assert max_memory < 500, f"Uso de memória excessivo: {max_memory:.1f}MB"
        
        # Validação de crescimento linear
        for i in range(1, len(memory_usage)):
            prev = memory_usage[i-1]
            curr = memory_usage[i]
            
            # Memória deve crescer de forma aproximadamente linear
            if prev['memory_increase'] > 0:
                memory_ratio = curr['memory_increase'] / prev['memory_increase']
                assert memory_ratio < 5, f"Crescimento de memória não linear: {memory_ratio:.2f}x"
            else:
                # Se o aumento anterior foi 0, apenas verifica que o atual não é muito grande
                assert curr['memory_increase'] < 10, f"Aumento de memória muito grande: {curr['memory_increase']:.1f}MB"
        
        print(f"\nLimites de memória validados: máximo {max_memory:.1f}MB")
    
    def test_csv_loading_performance(self, scaling_graphs):
        """
        Testa performance de carregamento de CSV.
        Teste automatizado: 80% gerado por IA
        """
        csv_path = "data/test_performance.csv"
        
        # Remove arquivo existente
        if os.path.exists(csv_path):
            os.remove(csv_path)
        
        loading_times = []
        
        for size, G in scaling_graphs.items():
            # Testa pré-cálculo
            start_time = time.time()
            lines_written = precompute_distances(
                G, 
                k_sample=min(5, size), 
                out_path=csv_path, 
                resume=False
            )
            elapsed = time.time() - start_time
            
            loading_times.append({
                'size': size,
                'nodes': G.number_of_nodes(),
                'lines_written': lines_written,
                'time': elapsed
            })
            
            print(f"Grafo {size}x{size}: {lines_written} linhas em {elapsed:.3f}s")
        
        # Validação de performance
        for usage in loading_times:
            assert usage['time'] < 10, f"Carregamento muito lento: {usage['time']:.3f}s"
        
        # Validação de escalabilidade
        for i in range(1, len(loading_times)):
            prev = loading_times[i-1]
            curr = loading_times[i]
            
            if prev['time'] > 0:
                time_ratio = curr['time'] / prev['time']
                assert time_ratio < 10, f"Escalabilidade ruim: {time_ratio:.2f}x"
            else:
                # Se o tempo anterior foi 0, apenas verifica que o atual não é muito grande
                assert curr['time'] < 1.0, f"Tempo muito alto: {curr['time']:.3f}s"
        
        print(f"\nPerformance de CSV validada: {len(loading_times)} testes")
        
        # Limpa arquivo de teste
        if os.path.exists(csv_path):
            os.remove(csv_path)
    
    def test_priority_queue_scaling(self):
        """
        Testa escalabilidade da PriorityQueue com diferentes tamanhos.
        Teste automatizado: 90% gerado por IA
        """
        sizes = [100, 500, 1000, 2000]
        results = []
        
        for size in sizes:
            pq = PriorityQueue()
            
            # Testa inserção
            start_time = time.time()
            for i in range(size):
                pq.insert(f"item_{i}", random.uniform(0, 1000))
            insert_time = time.time() - start_time
            
            # Testa extração
            start_time = time.time()
            extracted = []
            while not pq.is_empty():
                extracted.append(pq.extract_min())
            extract_time = time.time() - start_time
            
            results.append({
                'size': size,
                'insert_time': insert_time,
                'extract_time': extract_time,
                'total_time': insert_time + extract_time
            })
            
            print(f"Tamanho {size}: inserção={insert_time:.3f}s, extração={extract_time:.3f}s")
        
        # Validação de escalabilidade
        for i in range(1, len(results)):
            prev = results[i-1]
            curr = results[i]
            
            # Tempo deve crescer de forma aproximadamente logarítmica
            if prev['total_time'] > 0:
                time_ratio = curr['total_time'] / prev['total_time']
                assert time_ratio < 15, f"Escalabilidade ruim: {time_ratio:.2f}x"
            else:
                # Se o tempo anterior foi 0, apenas verifica que o atual não é muito grande
                assert curr['total_time'] < 2.0, f"Tempo muito alto: {curr['total_time']:.3f}s"
        
        print(f"\nEscalabilidade da PriorityQueue validada: {len(results)} tamanhos")
    
    def test_memory_scaling_validation(self, scaling_graphs):
        """
        Valida crescimento linear de memória.
        Teste automatizado: 85% gerado por IA
        """
        process = psutil.Process(os.getpid())
        memory_data = []
        
        for size, G in scaling_graphs.items():
            # Mede memória antes
            before_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Executa operações
            start = "0_0"
            end = f"{size-1}_{size-1}"
            
            # Dijkstra
            dijkstra(G, start, end)
            dijkstra_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # A*
            a_star(G, start, end)
            astar_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            memory_data.append({
                'size': size,
                'nodes': G.number_of_nodes(),
                'dijkstra_memory': dijkstra_memory - before_memory,
                'astar_memory': astar_memory - dijkstra_memory,
                'total_memory': astar_memory - before_memory
            })
            
            print(f"Grafo {size}x{size}: +{memory_data[-1]['total_memory']:.1f}MB")
        
        # Validação de crescimento linear
        for i in range(1, len(memory_data)):
            prev = memory_data[i-1]
            curr = memory_data[i]
            
            # Memória deve crescer de forma aproximadamente linear
            if prev['total_memory'] > 0:
                memory_ratio = curr['total_memory'] / prev['total_memory']
                assert memory_ratio < 3, f"Crescimento não linear: {memory_ratio:.2f}x"
            else:
                # Se o aumento anterior foi 0, apenas verifica que o atual não é muito grande
                assert curr['total_memory'] < 5, f"Aumento de memória muito grande: {curr['total_memory']:.1f}MB"
        
        print(f"\nCrescimento linear de memória validado: {len(memory_data)} pontos")
