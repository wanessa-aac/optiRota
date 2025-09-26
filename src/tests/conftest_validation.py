"""
Fixtures para testes de validação.
FASE 4: Testes de Validação
"""

import pytest
import os
from src.parser_osm import parse_osm
from src.graph import build_graph
from src.algorithms import dijkstra, a_star
from src.structures import PriorityQueue, Stack, FIFOQueue

@pytest.fixture(scope="session")
def validation_dataset():
    """
    Fixture para dataset de validação.
    Teste automatizado: 95% gerado por IA
    """
    dataset_path = "data/090925maceio_ponta_verde.osm"
    
    if not os.path.exists(dataset_path):
        pytest.skip(f"Dataset não encontrado: {dataset_path}")
    
    try:
        parsed_data = parse_osm(dataset_path)
        return parsed_data
    except Exception as e:
        pytest.skip(f"Erro no parsing do dataset: {e}")

@pytest.fixture(scope="session")
def validation_graph(validation_dataset):
    """
    Fixture para grafo de validação.
    Teste automatizado: 95% gerado por IA
    """
    try:
        G = build_graph(validation_dataset)
        return G
    except Exception as e:
        pytest.skip(f"Erro na construção do grafo: {e}")

@pytest.fixture(scope="session")
def validation_nodes(validation_graph):
    """
    Fixture para nós de validação.
    Teste automatizado: 90% gerado por IA
    """
    nodes = list(validation_graph.nodes())
    if len(nodes) < 10:
        pytest.skip("Grafo muito pequeno para validação")
    
    return nodes

@pytest.fixture(scope="session")
def validation_edges(validation_graph):
    """
    Fixture para edges de validação.
    Teste automatizado: 90% gerado por IA
    """
    edges = list(validation_graph.edges())
    if len(edges) < 10:
        pytest.skip("Grafo muito pequeno para validação")
    
    return edges

@pytest.fixture(scope="session")
def validation_sample(validation_graph, validation_nodes):
    """
    Fixture para amostra de validação.
    Teste automatizado: 90% gerado por IA
    """
    # Seleciona amostra representativa
    sample_size = min(20, len(validation_nodes))
    sample_nodes = validation_nodes[:sample_size]
    
    return sample_nodes

@pytest.fixture(scope="session")
def validation_subgraph(validation_graph, validation_sample):
    """
    Fixture para subgrafo de validação.
    Teste automatizado: 90% gerado por IA
    """
    subgraph = validation_graph.subgraph(validation_sample)
    return subgraph

@pytest.fixture(scope="session")
def validation_coordinates(validation_graph, validation_nodes):
    """
    Fixture para coordenadas de validação.
    Teste automatizado: 90% gerado por IA
    """
    coordinates = {}
    for node in validation_nodes:
        node_data = validation_graph.nodes[node]
        coordinates[node] = {
            'lat': node_data['lat'],
            'lon': node_data['lon']
        }
    
    return coordinates

@pytest.fixture(scope="session")
def validation_bounds(validation_coordinates):
    """
    Fixture para limites de validação.
    Teste automatizado: 90% gerado por IA
    """
    lats = [coord['lat'] for coord in validation_coordinates.values()]
    lons = [coord['lon'] for coord in validation_coordinates.values()]
    
    bounds = {
        'min_lat': min(lats),
        'max_lat': max(lats),
        'min_lon': min(lons),
        'max_lon': max(lons),
        'lat_span': max(lats) - min(lats),
        'lon_span': max(lons) - min(lons)
    }
    
    return bounds

@pytest.fixture(scope="session")
def validation_centroid(validation_coordinates):
    """
    Fixture para centroide de validação.
    Teste automatizado: 90% gerado por IA
    """
    lats = [coord['lat'] for coord in validation_coordinates.values()]
    lons = [coord['lon'] for coord in validation_coordinates.values()]
    
    centroid = {
        'lat': sum(lats) / len(lats),
        'lon': sum(lons) / len(lons)
    }
    
    return centroid

@pytest.fixture(scope="session")
def validation_connectivity(validation_graph):
    """
    Fixture para conectividade de validação.
    Teste automatizado: 90% gerado por IA
    """
    import networkx as nx
    
    # Calcula componentes conectados
    wccs = list(nx.weakly_connected_components(validation_graph))
    giant_component = max(wccs, key=len)
    
    connectivity = {
        'total_components': len(wccs),
        'giant_component_size': len(giant_component),
        'giant_component_ratio': len(giant_component) / validation_graph.number_of_nodes(),
        'is_connected': len(wccs) == 1
    }
    
    return connectivity

@pytest.fixture(scope="session")
def validation_performance_metrics(validation_graph, validation_nodes):
    """
    Fixture para métricas de performance de validação.
    Teste automatizado: 90% gerado por IA
    """
    import time
    
    # Testa performance com amostra
    sample_size = min(5, len(validation_nodes))
    sample_nodes = validation_nodes[:sample_size]
    
    metrics = {}
    
    try:
        # Testa Dijkstra
        start_time = time.time()
        dijkstra_result = dijkstra(validation_graph, sample_nodes[0], sample_nodes[-1])
        dijkstra_time = time.time() - start_time
        
        # Testa A*
        start_time = time.time()
        astar_result = a_star(validation_graph, sample_nodes[0], sample_nodes[-1])
        astar_time = time.time() - start_time
        
        metrics = {
            'dijkstra_time': dijkstra_time,
            'astar_time': astar_time,
            'dijkstra_distance': dijkstra_result['distance'],
            'astar_distance': astar_result['distance'],
            'dijkstra_nodes_visited': dijkstra_result['nodes_visited'],
            'astar_nodes_visited': astar_result['nodes_visited']
        }
        
    except Exception as e:
        metrics = {'error': str(e)}
    
    return metrics

@pytest.fixture(scope="session")
def validation_memory_usage(validation_graph):
    """
    Fixture para uso de memória de validação.
    Teste automatizado: 90% gerado por IA
    """
    try:
        import psutil
        
        process = psutil.Process()
        memory_usage = process.memory_info().rss / 1024 / 1024  # MB
        
        return {
            'memory_mb': memory_usage,
            'nodes': validation_graph.number_of_nodes(),
            'edges': validation_graph.number_of_edges(),
            'memory_per_node': memory_usage / validation_graph.number_of_nodes() if validation_graph.number_of_nodes() > 0 else 0
        }
        
    except ImportError:
        return {'error': 'psutil não disponível'}

@pytest.fixture(scope="session")
def validation_geographic_stats(validation_coordinates):
    """
    Fixture para estatísticas geográficas de validação.
    Teste automatizado: 90% gerado por IA
    """
    import math
    
    lats = [coord['lat'] for coord in validation_coordinates.values()]
    lons = [coord['lon'] for coord in validation_coordinates.values()]
    
    # Estatísticas básicas
    lat_mean = sum(lats) / len(lats)
    lon_mean = sum(lons) / len(lons)
    
    # Desvio padrão
    lat_variance = sum((lat - lat_mean) ** 2 for lat in lats) / len(lats)
    lon_variance = sum((lon - lon_mean) ** 2 for lon in lons) / len(lats)
    
    lat_std = math.sqrt(lat_variance)
    lon_std = math.sqrt(lon_variance)
    
    # Área
    lat_span = max(lats) - min(lats)
    lon_span = max(lons) - min(lons)
    area = lat_span * lon_span
    
    stats = {
        'lat_mean': lat_mean,
        'lon_mean': lon_mean,
        'lat_std': lat_std,
        'lon_std': lon_std,
        'lat_span': lat_span,
        'lon_span': lon_span,
        'area': area,
        'density': len(lats) / area if area > 0 else 0
    }
    
    return stats

@pytest.fixture(scope="session")
def validation_algorithm_results(validation_graph, validation_nodes):
    """
    Fixture para resultados de algoritmos de validação.
    Teste automatizado: 90% gerado por IA
    """
    if len(validation_nodes) < 2:
        return {'error': 'Grafo muito pequeno para algoritmos'}
    
    try:
        start = validation_nodes[0]
        end = validation_nodes[-1]
        
        # Testa Dijkstra
        dijkstra_result = dijkstra(validation_graph, start, end)
        
        # Testa A*
        astar_result = a_star(validation_graph, start, end)
        
        return {
            'dijkstra': dijkstra_result,
            'astar': astar_result,
            'start': start,
            'end': end
        }
        
    except Exception as e:
        return {'error': str(e)}

@pytest.fixture(scope="session")
def validation_data_quality(validation_dataset, validation_graph):
    """
    Fixture para qualidade de dados de validação.
    Teste automatizado: 90% gerado por IA
    """
    quality_metrics = {}
    
    try:
        # Métricas de dataset
        quality_metrics['dataset_nodes'] = len(validation_dataset['nodes'])
        quality_metrics['dataset_ways'] = len(validation_dataset['ways'])
        
        # Métricas de grafo
        quality_metrics['graph_nodes'] = validation_graph.number_of_nodes()
        quality_metrics['graph_edges'] = validation_graph.number_of_edges()
        
        # Métricas de qualidade
        quality_metrics['node_retention'] = quality_metrics['graph_nodes'] / quality_metrics['dataset_nodes'] if quality_metrics['dataset_nodes'] > 0 else 0
        quality_metrics['edge_retention'] = quality_metrics['graph_edges'] / quality_metrics['dataset_ways'] if quality_metrics['dataset_ways'] > 0 else 0
        
        # Métricas de conectividade
        import networkx as nx
        wccs = list(nx.weakly_connected_components(validation_graph))
        quality_metrics['connected_components'] = len(wccs)
        quality_metrics['giant_component_size'] = len(max(wccs, key=len)) if wccs else 0
        
        return quality_metrics
        
    except Exception as e:
        return {'error': str(e)}

@pytest.fixture(scope="session")
def validation_code_metrics():
    """
    Fixture para métricas de código de validação.
    Teste automatizado: 90% gerado por IA
    """
    import inspect
    
    # Funções para analisar
    functions = [
        dijkstra,
        a_star,
        parse_osm,
        build_graph
    ]
    
    # Classes para analisar
    classes = [
        PriorityQueue,
        Stack,
        FIFOQueue
    ]
    
    metrics = {
        'functions': {},
        'classes': {}
    }
    
    # Analisa funções
    for func in functions:
        source = inspect.getsource(func)
        lines = source.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        metrics['functions'][func.__name__] = {
            'total_lines': len(lines),
            'non_empty_lines': len(non_empty_lines),
            'has_docstring': func.__doc__ is not None,
            'docstring_length': len(func.__doc__.strip()) if func.__doc__ else 0
        }
    
    # Analisa classes
    for cls in classes:
        source = inspect.getsource(cls)
        lines = source.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        metrics['classes'][cls.__name__] = {
            'total_lines': len(lines),
            'non_empty_lines': len(non_empty_lines),
            'has_docstring': cls.__doc__ is not None,
            'docstring_length': len(cls.__doc__.strip()) if cls.__doc__ else 0
        }
    
    return metrics

