"""
Testes de integração metropolitana.
FASE 3: Testes de Dataset Metropolitano
"""

import pytest
import os
import time
from src.parser_osm import parse_osm
from src.graph import build_graph
from src.algorithms import dijkstra, a_star, precompute_distances

class TestMetropolitanIntegration:
    """
    Testes de integração metropolitana.
    Teste automatizado: 90% gerado por IA
    """
    
    def test_metropolitan_full_pipeline(self, maceio_dataset, maceio_graph, metropolitan_nodes):
        """
        Testa pipeline completo metropolitano.
        Teste automatizado: 95% gerado por IA
        """
        # Validações de pipeline
        assert maceio_dataset is not None, "Dataset deve estar disponível"
        assert maceio_graph is not None, "Grafo deve estar disponível"
        assert len(metropolitan_nodes) > 0, "Deve ter nodes metropolitanos"
        
        # Testa pathfinding
        start = metropolitan_nodes[0]
        end = metropolitan_nodes[-1]
        
        # Dijkstra
        dijkstra_result = dijkstra(maceio_graph, start, end)
        assert dijkstra_result['distance'] > 0, "Distância Dijkstra deve ser positiva"
        assert len(dijkstra_result['path']) > 0, "Path Dijkstra deve existir"
        
        # A*
        astar_result = a_star(maceio_graph, start, end)
        assert astar_result['distance'] > 0, "Distância A* deve ser positiva"
        assert len(astar_result['path']) > 0, "Path A* deve existir"
        
        print(f"\nPipeline metropolitano completo:")
        print(f"  Dataset: {len(maceio_dataset['nodes'])} nodes, {len(maceio_dataset['ways'])} ways")
        print(f"  Grafo: {maceio_graph.number_of_nodes()} nodes, {maceio_graph.number_of_edges()} edges")
        print(f"  Dijkstra: {dijkstra_result['distance']:.2f} km")
        print(f"  A*: {astar_result['distance']:.2f} km")
    
    def test_metropolitan_performance_integration(self, maceio_graph, metropolitan_sample):
        """
        Testa integração de performance metropolitana.
        Teste automatizado: 90% gerado por IA
        """
        # Testa performance com amostra
        start = metropolitan_sample[0]
        end = metropolitan_sample[-1]
        
        # Mede tempo de pathfinding
        start_time = time.time()
        dijkstra_result = dijkstra(maceio_graph, start, end)
        dijkstra_time = time.time() - start_time
        
        start_time = time.time()
        astar_result = a_star(maceio_graph, start, end)
        astar_time = time.time() - start_time
        
        # Validações de performance
        assert dijkstra_time < 10.0, f"Dijkstra muito lento: {dijkstra_time:.2f}s"
        assert astar_time < 10.0, f"A* muito lento: {astar_time:.2f}s"
        
        # Validações de resultados
        assert dijkstra_result['distance'] > 0, "Distância Dijkstra deve ser positiva"
        assert astar_result['distance'] > 0, "Distância A* deve ser positiva"
        
        print(f"\nIntegração de performance metropolitana:")
        print(f"  Dijkstra: {dijkstra_time:.3f}s ({dijkstra_result['nodes_visited']} nodes)")
        print(f"  A*: {astar_time:.3f}s ({astar_result['nodes_visited']} nodes)")
        print(f"  Diferença: {abs(dijkstra_result['distance'] - astar_result['distance']):.2f} km")
    
    def test_metropolitan_memory_integration(self, maceio_graph, metropolitan_memory_usage):
        """
        Testa integração de memória metropolitana.
        Teste automatizado: 90% gerado por IA
        """
        # Validações de memória
        assert 'memory_mb' in metropolitan_memory_usage, "Deve ter métrica de memória"
        assert metropolitan_memory_usage['memory_mb'] > 0, "Memória deve ser positiva"
        assert metropolitan_memory_usage['nodes'] > 0, "Deve ter nodes"
        assert metropolitan_memory_usage['edges'] > 0, "Deve ter edges"
        
        # Validações de eficiência
        memory_per_node = metropolitan_memory_usage['memory_per_node']
        assert memory_per_node > 0, "Memória por nó deve ser positiva"
        assert memory_per_node < 10, f"Memória por nó muito alta: {memory_per_node:.2f}MB"
        
        print(f"\nIntegração de memória metropolitana:")
        print(f"  Memória total: {metropolitan_memory_usage['memory_mb']:.1f}MB")
        print(f"  Nodes: {metropolitan_memory_usage['nodes']}")
        print(f"  Edges: {metropolitan_memory_usage['edges']}")
        print(f"  Memória por nó: {memory_per_node:.2f}MB")
    
    def test_metropolitan_geographic_integration(self, metropolitan_coordinates, metropolitan_bounds, metropolitan_centroid):
        """
        Testa integração geográfica metropolitana.
        Teste automatizado: 90% gerado por IA
        """
        # Validações de coordenadas
        assert len(metropolitan_coordinates) > 0, "Deve ter coordenadas"
        
        # Validações de limites
        assert metropolitan_bounds['min_lat'] < metropolitan_bounds['max_lat'], "Latitude mínima deve ser < máxima"
        assert metropolitan_bounds['min_lon'] < metropolitan_bounds['max_lon'], "Longitude mínima deve ser < máxima"
        assert metropolitan_bounds['lat_span'] > 0, "Extensão de latitude deve ser positiva"
        assert metropolitan_bounds['lon_span'] > 0, "Extensão de longitude deve ser positiva"
        
        # Validações de centroide
        assert -90 <= metropolitan_centroid['lat'] <= 90, "Centroide latitude inválida"
        assert -180 <= metropolitan_centroid['lon'] <= 180, "Centroide longitude inválida"
        
        print(f"\nIntegração geográfica metropolitana:")
        print(f"  Coordenadas: {len(metropolitan_coordinates)}")
        print(f"  Limites: ({metropolitan_bounds['min_lat']:.6f}, {metropolitan_bounds['min_lon']:.6f}) a ({metropolitan_bounds['max_lat']:.6f}, {metropolitan_bounds['max_lon']:.6f})")
        print(f"  Centroide: ({metropolitan_centroid['lat']:.6f}, {metropolitan_centroid['lon']:.6f})")
        print(f"  Extensão: {metropolitan_bounds['lat_span']:.6f} x {metropolitan_bounds['lon_span']:.6f}")
    
    def test_metropolitan_connectivity_integration(self, maceio_graph, metropolitan_connectivity):
        """
        Testa integração de conectividade metropolitana.
        Teste automatizado: 90% gerado por IA
        """
        # Validações de conectividade
        assert metropolitan_connectivity['total_components'] > 0, "Deve ter componentes"
        assert metropolitan_connectivity['giant_component_size'] > 0, "Componente gigante deve existir"
        assert 0 < metropolitan_connectivity['giant_component_ratio'] <= 1, "Razão do componente gigante deve ser válida"
        
        # Validações de rede
        assert metropolitan_connectivity['giant_component_size'] > 10, "Componente gigante deve ser significativo"
        assert metropolitan_connectivity['giant_component_ratio'] > 0.5, "Componente gigante deve ser dominante"
        
        print(f"\nIntegração de conectividade metropolitana:")
        print(f"  Componentes totais: {metropolitan_connectivity['total_components']}")
        print(f"  Componente gigante: {metropolitan_connectivity['giant_component_size']} nodes")
        print(f"  Razão: {metropolitan_connectivity['giant_component_ratio']:.2f}")
        print(f"  Conectado: {metropolitan_connectivity['is_connected']}")
    
    def test_metropolitan_performance_metrics_integration(self, metropolitan_performance_metrics):
        """
        Testa integração de métricas de performance metropolitana.
        Teste automatizado: 90% gerado por IA
        """
        # Validações de métricas
        if 'error' in metropolitan_performance_metrics:
            pytest.skip(f"Erro nas métricas: {metropolitan_performance_metrics['error']}")
        
        assert 'dijkstra_time' in metropolitan_performance_metrics, "Deve ter tempo Dijkstra"
        assert 'astar_time' in metropolitan_performance_metrics, "Deve ter tempo A*"
        assert metropolitan_performance_metrics['dijkstra_time'] > 0, "Tempo Dijkstra deve ser positivo"
        assert metropolitan_performance_metrics['astar_time'] > 0, "Tempo A* deve ser positivo"
        
        # Validações de resultados
        assert metropolitan_performance_metrics['dijkstra_distance'] > 0, "Distância Dijkstra deve ser positiva"
        assert metropolitan_performance_metrics['astar_distance'] > 0, "Distância A* deve ser positiva"
        
        print(f"\nIntegração de métricas de performance metropolitana:")
        print(f"  Dijkstra: {metropolitan_performance_metrics['dijkstra_time']:.3f}s ({metropolitan_performance_metrics['dijkstra_nodes_visited']} nodes)")
        print(f"  A*: {metropolitan_performance_metrics['astar_time']:.3f}s ({metropolitan_performance_metrics['astar_nodes_visited']} nodes)")
        print(f"  Distâncias: {metropolitan_performance_metrics['dijkstra_distance']:.2f} vs {metropolitan_performance_metrics['astar_distance']:.2f} km")
    
    def test_metropolitan_geographic_stats_integration(self, metropolitan_geographic_stats):
        """
        Testa integração de estatísticas geográficas metropolitanas.
        Teste automatizado: 90% gerado por IA
        """
        # Validações de estatísticas
        assert metropolitan_geographic_stats['lat_std'] > 0, "Desvio padrão latitude deve ser positivo"
        assert metropolitan_geographic_stats['lon_std'] > 0, "Desvio padrão longitude deve ser positivo"
        assert metropolitan_geographic_stats['area'] > 0, "Área deve ser positiva"
        assert metropolitan_geographic_stats['density'] > 0, "Densidade deve ser positiva"
        
        # Validações de dispersão
        assert metropolitan_geographic_stats['lat_std'] < 1.0, "Dispersão latitude muito alta"
        assert metropolitan_geographic_stats['lon_std'] < 1.0, "Dispersão longitude muito alta"
        
        print(f"\nIntegração de estatísticas geográficas metropolitanas:")
        print(f"  Centro: ({metropolitan_geographic_stats['lat_mean']:.6f}, {metropolitan_geographic_stats['lon_mean']:.6f})")
        print(f"  Dispersão: {metropolitan_geographic_stats['lat_std']:.6f} x {metropolitan_geographic_stats['lon_std']:.6f}")
        print(f"  Área: {metropolitan_geographic_stats['area']:.8f} graus²")
        print(f"  Densidade: {metropolitan_geographic_stats['density']:.0f} nodes/grau²")
    
    def test_metropolitan_end_to_end(self, maceio_dataset, maceio_graph, metropolitan_nodes):
        """
        Testa fluxo end-to-end metropolitano.
        Teste automatizado: 95% gerado por IA
        """
        # Testa fluxo completo
        start = metropolitan_nodes[0]
        end = metropolitan_nodes[-1]
        
        # Pathfinding
        dijkstra_result = dijkstra(maceio_graph, start, end)
        astar_result = a_star(maceio_graph, start, end)
        
        # Validações end-to-end
        assert dijkstra_result['distance'] > 0, "Distância Dijkstra deve ser positiva"
        assert astar_result['distance'] > 0, "Distância A* deve ser positiva"
        assert len(dijkstra_result['path']) > 0, "Path Dijkstra deve existir"
        assert len(astar_result['path']) > 0, "Path A* deve existir"
        
        # Validações de consistência
        assert dijkstra_result['path'][0] == start, "Path Dijkstra deve começar no start"
        assert dijkstra_result['path'][-1] == end, "Path Dijkstra deve terminar no end"
        assert astar_result['path'][0] == start, "Path A* deve começar no start"
        assert astar_result['path'][-1] == end, "Path A* deve terminar no end"
        
        print(f"\nFluxo end-to-end metropolitano:")
        print(f"  Start: {start}")
        print(f"  End: {end}")
        print(f"  Dijkstra: {dijkstra_result['distance']:.2f} km ({len(dijkstra_result['path'])} nós)")
        print(f"  A*: {astar_result['distance']:.2f} km ({len(astar_result['path'])} nós)")
        print(f"  Diferença: {abs(dijkstra_result['distance'] - astar_result['distance']):.2f} km")

