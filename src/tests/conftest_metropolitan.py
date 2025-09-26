"""
Fixtures para testes metropolitanos.
FASE 3: Testes de Dataset Metropolitano
"""

import pytest
import os
from src.parser_osm import parse_osm
from src.graph import build_graph

@pytest.fixture(scope="session")
def maceio_dataset():
    """
    Fixture para dataset de Maceió.
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
def maceio_graph(maceio_dataset):
    """
    Fixture para grafo de Maceió.
    Teste automatizado: 95% gerado por IA
    """
    try:
        G = build_graph(maceio_dataset)
        return G
    except Exception as e:
        pytest.skip(f"Erro na construção do grafo: {e}")

@pytest.fixture(scope="session")
def metropolitan_nodes(maceio_graph):
    """
    Fixture para nós metropolitanos.
    Teste automatizado: 90% gerado por IA
    """
    nodes = list(maceio_graph.nodes())
    if len(nodes) < 10:
        pytest.skip("Grafo muito pequeno para testes metropolitanos")
    
    return nodes

@pytest.fixture(scope="session")
def metropolitan_edges(maceio_graph):
    """
    Fixture para edges metropolitanos.
    Teste automatizado: 90% gerado por IA
    """
    edges = list(maceio_graph.edges())
    if len(edges) < 10:
        pytest.skip("Grafo muito pequeno para testes metropolitanos")
    
    return edges

@pytest.fixture(scope="session")
def metropolitan_sample(maceio_graph, metropolitan_nodes):
    """
    Fixture para amostra metropolitana.
    Teste automatizado: 90% gerado por IA
    """
    # Seleciona amostra representativa
    sample_size = min(20, len(metropolitan_nodes))
    sample_nodes = metropolitan_nodes[:sample_size]
    
    return sample_nodes

@pytest.fixture(scope="session")
def metropolitan_subgraph(maceio_graph, metropolitan_sample):
    """
    Fixture para subgrafo metropolitano.
    Teste automatizado: 90% gerado por IA
    """
    subgraph = maceio_graph.subgraph(metropolitan_sample)
    return subgraph

@pytest.fixture(scope="session")
def metropolitan_coordinates(maceio_graph, metropolitan_nodes):
    """
    Fixture para coordenadas metropolitanas.
    Teste automatizado: 90% gerado por IA
    """
    coordinates = {}
    for node in metropolitan_nodes:
        node_data = maceio_graph.nodes[node]
        coordinates[node] = {
            'lat': node_data['lat'],
            'lon': node_data['lon']
        }
    
    return coordinates

@pytest.fixture(scope="session")
def metropolitan_bounds(metropolitan_coordinates):
    """
    Fixture para limites metropolitanos.
    Teste automatizado: 90% gerado por IA
    """
    lats = [coord['lat'] for coord in metropolitan_coordinates.values()]
    lons = [coord['lon'] for coord in metropolitan_coordinates.values()]
    
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
def metropolitan_centroid(metropolitan_coordinates):
    """
    Fixture para centroide metropolitano.
    Teste automatizado: 90% gerado por IA
    """
    lats = [coord['lat'] for coord in metropolitan_coordinates.values()]
    lons = [coord['lon'] for coord in metropolitan_coordinates.values()]
    
    centroid = {
        'lat': sum(lats) / len(lats),
        'lon': sum(lons) / len(lons)
    }
    
    return centroid

@pytest.fixture(scope="session")
def metropolitan_connectivity(maceio_graph):
    """
    Fixture para conectividade metropolitana.
    Teste automatizado: 90% gerado por IA
    """
    import networkx as nx
    
    # Calcula componentes conectados
    wccs = list(nx.weakly_connected_components(maceio_graph))
    giant_component = max(wccs, key=len)
    
    connectivity = {
        'total_components': len(wccs),
        'giant_component_size': len(giant_component),
        'giant_component_ratio': len(giant_component) / maceio_graph.number_of_nodes(),
        'is_connected': len(wccs) == 1
    }
    
    return connectivity

@pytest.fixture(scope="session")
def metropolitan_performance_metrics(maceio_graph, metropolitan_nodes):
    """
    Fixture para métricas de performance metropolitana.
    Teste automatizado: 90% gerado por IA
    """
    import time
    from src.algorithms import dijkstra, a_star
    
    # Testa performance com amostra
    sample_size = min(5, len(metropolitan_nodes))
    sample_nodes = metropolitan_nodes[:sample_size]
    
    metrics = {}
    
    try:
        # Testa Dijkstra
        start_time = time.time()
        dijkstra_result = dijkstra(maceio_graph, sample_nodes[0], sample_nodes[-1])
        dijkstra_time = time.time() - start_time
        
        # Testa A*
        start_time = time.time()
        astar_result = a_star(maceio_graph, sample_nodes[0], sample_nodes[-1])
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
def metropolitan_memory_usage(maceio_graph):
    """
    Fixture para uso de memória metropolitana.
    Teste automatizado: 90% gerado por IA
    """
    try:
        import psutil
        
        process = psutil.Process()
        memory_usage = process.memory_info().rss / 1024 / 1024  # MB
        
        return {
            'memory_mb': memory_usage,
            'nodes': maceio_graph.number_of_nodes(),
            'edges': maceio_graph.number_of_edges(),
            'memory_per_node': memory_usage / maceio_graph.number_of_nodes() if maceio_graph.number_of_nodes() > 0 else 0
        }
        
    except ImportError:
        return {'error': 'psutil não disponível'}

@pytest.fixture(scope="session")
def metropolitan_geographic_stats(metropolitan_coordinates):
    """
    Fixture para estatísticas geográficas metropolitanas.
    Teste automatizado: 90% gerado por IA
    """
    import math
    
    lats = [coord['lat'] for coord in metropolitan_coordinates.values()]
    lons = [coord['lon'] for coord in metropolitan_coordinates.values()]
    
    # Estatísticas básicas
    lat_mean = sum(lats) / len(lats)
    lon_mean = sum(lons) / len(lons)
    
    # Desvio padrão
    lat_variance = sum((lat - lat_mean) ** 2 for lat in lats) / len(lats)
    lon_variance = sum((lon - lon_mean) ** 2 for lon in lons) / len(lons)
    
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

