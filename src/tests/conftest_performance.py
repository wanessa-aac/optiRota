# src/tests/conftest_performance.py
"""
Configurações e fixtures para testes de performance.
FASE 1: Testes de Performance - 90% automatizável com IA
"""

import pytest
import time
import random
import networkx as nx
import psutil
import os
from src.structures import PriorityQueue


class PerformanceMonitor:
    """Monitor de performance para testes."""
    
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.initial_memory = self.process.memory_info().rss / 1024 / 1024  # MB
    
    def get_memory_usage(self):
        """Retorna uso atual de memória em MB."""
        return self.process.memory_info().rss / 1024 / 1024
    
    def get_memory_increase(self):
        """Retorna aumento de memória desde a inicialização."""
        return self.get_memory_usage() - self.initial_memory
    
    def get_cpu_usage(self):
        """Retorna uso atual de CPU."""
        return self.process.cpu_percent()


@pytest.fixture
def performance_monitor():
    """Fixture para monitor de performance."""
    return PerformanceMonitor()


@pytest.fixture
def benchmark_config():
    """Configuração para benchmarks."""
    return {
        'min_rounds': 3,
        'max_time': 10.0,
        'warmup': True,
        'memory_limit_mb': 500,
        'timeout_seconds': 30
    }


@pytest.fixture
def small_graph():
    """Grafo pequeno para testes básicos."""
    G = nx.DiGraph()
    
    # Cria grafo 5x5
    for i in range(5):
        for j in range(5):
            node_id = f"{i}_{j}"
            G.add_node(node_id, lat=i, lon=j)
            
            if j < 4:
                right_id = f"{i}_{j+1}"
                G.add_edge(node_id, right_id, weight=1.0)
            
            if i < 4:
                down_id = f"{i+1}_{j}"
                G.add_edge(node_id, down_id, weight=1.0)
    
    return G


@pytest.fixture
def medium_graph():
    """Grafo médio para testes de performance."""
    G = nx.DiGraph()
    
    # Cria grafo 10x10
    for i in range(10):
        for j in range(10):
            node_id = f"{i}_{j}"
            G.add_node(node_id, lat=i, lon=j)
            
            if j < 9:
                right_id = f"{i}_{j+1}"
                weight = random.uniform(0.1, 2.0)
                G.add_edge(node_id, right_id, weight=weight)
            
            if i < 9:
                down_id = f"{i+1}_{j}"
                weight = random.uniform(0.1, 2.0)
                G.add_edge(node_id, down_id, weight=weight)
    
    return G


@pytest.fixture
def large_graph():
    """Grafo grande para testes de escalabilidade."""
    G = nx.DiGraph()
    
    # Cria grafo 20x20
    for i in range(20):
        for j in range(20):
            node_id = f"{i}_{j}"
            G.add_node(node_id, lat=i, lon=j)
            
            if j < 19:
                right_id = f"{i}_{j+1}"
                weight = random.uniform(0.1, 2.0)
                G.add_edge(node_id, right_id, weight=weight)
            
            if i < 19:
                down_id = f"{i+1}_{j}"
                weight = random.uniform(0.1, 2.0)
                G.add_edge(node_id, down_id, weight=weight)
    
    return G


@pytest.fixture
def scaling_graphs():
    """Grafos de diferentes tamanhos para testes de escalabilidade."""
    graphs = {}
    
    for size in [5, 10, 15, 20]:
        G = nx.DiGraph()
        for i in range(size):
            for j in range(size):
                node_id = f"{i}_{j}"
                G.add_node(node_id, lat=i, lon=j)
                
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


@pytest.fixture
def priority_queue_fixture():
    """Fixture para PriorityQueue com dados de teste."""
    pq = PriorityQueue()
    
    # Adiciona alguns elementos
    for i in range(10):
        pq.insert(f"item_{i}", random.uniform(0, 100))
    
    return pq


@pytest.fixture
def performance_thresholds():
    """Thresholds de performance para validação."""
    return {
        'dijkstra_max_time': 5.0,  # segundos
        'astar_max_time': 5.0,     # segundos
        'priority_queue_max_time': 2.0,  # segundos
        'memory_max_increase': 100,  # MB
        'cpu_max_usage': 80,  # percentual
        'scaling_max_ratio': 10.0  # razão máxima entre tamanhos
    }


@pytest.fixture
def test_data_generator():
    """Gerador de dados de teste."""
    class TestDataGenerator:
        def __init__(self):
            self.random = random.Random(42)  # Seed fixa para reprodutibilidade
        
        def generate_coordinates(self, num_points):
            """Gera coordenadas aleatórias."""
            return [
                (self.random.uniform(-90, 90), self.random.uniform(-180, 180))
                for _ in range(num_points)
            ]
        
        def generate_weights(self, num_edges):
            """Gera pesos aleatórios para arestas."""
            return [self.random.uniform(0.1, 10.0) for _ in range(num_edges)]
        
        def generate_priorities(self, num_items):
            """Gera prioridades aleatórias."""
            return [self.random.uniform(0, 1000) for _ in range(num_items)]
    
    return TestDataGenerator()


@pytest.fixture
def performance_logger():
    """Logger para testes de performance."""
    import logging
    
    logger = logging.getLogger('performance_tests')
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


# Marcadores para diferentes tipos de testes
pytestmark = [
    pytest.mark.performance,
    pytest.mark.benchmark,
    pytest.mark.slow
]
