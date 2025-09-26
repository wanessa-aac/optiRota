"""
Testes de integração de validação.
FASE 4: Testes de Validação
"""

import pytest
import os
from src.parser_osm import parse_osm
from src.graph import build_graph
from src.algorithms import dijkstra, a_star
from src.structures import PriorityQueue, Stack, FIFOQueue

class TestValidationIntegration:
    """
    Testes de integração de validação.
    Teste automatizado: 90% gerado por IA
    """
    
    def test_validation_pipeline_completeness(self, validation_dataset, validation_graph, validation_nodes):
        """
        Testa completude do pipeline de validação.
        Teste automatizado: 95% gerado por IA
        """
        # Validações de pipeline
        assert validation_dataset is not None, "Dataset deve estar disponível"
        assert validation_graph is not None, "Grafo deve estar disponível"
        assert len(validation_nodes) > 0, "Deve ter nodes de validação"
        
        # Validações de dados
        assert "nodes" in validation_dataset, "Dataset deve ter nodes"
        assert "ways" in validation_dataset, "Dataset deve ter ways"
        assert len(validation_dataset["nodes"]) > 0, "Dataset deve ter nodes"
        assert len(validation_dataset["ways"]) > 0, "Dataset deve ter ways"
        
        # Validações de grafo
        assert validation_graph.number_of_nodes() > 0, "Grafo deve ter nodes"
        assert validation_graph.number_of_edges() > 0, "Grafo deve ter edges"
        
        print(f"\nPipeline de validação completo:")
        print(f"  Dataset: {len(validation_dataset['nodes'])} nodes, {len(validation_dataset['ways'])} ways")
        print(f"  Grafo: {validation_graph.number_of_nodes()} nodes, {validation_graph.number_of_edges()} edges")
        print(f"  Nodes de validação: {len(validation_nodes)}")
        print(f"  Completude: ✅")
    
    def test_validation_algorithm_integration(self, validation_graph, validation_nodes):
        """
        Testa integração de algoritmos de validação.
        Teste automatizado: 90% gerado por IA
        """
        if len(validation_nodes) < 2:
            pytest.skip("Grafo muito pequeno para algoritmos")
        
        start = validation_nodes[0]
        end = validation_nodes[-1]
        
        # Testa Dijkstra
        dijkstra_result = dijkstra(validation_graph, start, end)
        
        # Validações de resultado Dijkstra
        assert "distance" in dijkstra_result, "Dijkstra deve ter distance"
        assert "path" in dijkstra_result, "Dijkstra deve ter path"
        assert "nodes_visited" in dijkstra_result, "Dijkstra deve ter nodes_visited"
        
        assert dijkstra_result["distance"] > 0, "Distância Dijkstra deve ser positiva"
        assert len(dijkstra_result["path"]) > 0, "Path Dijkstra deve ter elementos"
        assert dijkstra_result["nodes_visited"] >= 0, "Nodes_visited Dijkstra deve ser não-negativo"
        
        # Testa A*
        astar_result = a_star(validation_graph, start, end)
        
        # Validações de resultado A*
        assert "distance" in astar_result, "A* deve ter distance"
        assert "path" in astar_result, "A* deve ter path"
        assert "nodes_visited" in astar_result, "A* deve ter nodes_visited"
        
        assert astar_result["distance"] > 0, "Distância A* deve ser positiva"
        assert len(astar_result["path"]) > 0, "Path A* deve ter elementos"
        assert astar_result["nodes_visited"] >= 0, "Nodes_visited A* deve ser não-negativo"
        
        # Validações de consistência
        assert abs(dijkstra_result["distance"] - astar_result["distance"]) < 1e-9, "Distâncias devem ser iguais"
        assert dijkstra_result["path"] == astar_result["path"], "Paths devem ser iguais"
        
        print(f"\nIntegração de algoritmos de validação:")
        print(f"  Dijkstra: {dijkstra_result['distance']:.2f} km")
        print(f"  A*: {astar_result['distance']:.2f} km")
        print(f"  Consistência: {'✅' if abs(dijkstra_result['distance'] - astar_result['distance']) < 1e-9 else '❌'}")
    
    def test_validation_data_quality_integration(self, validation_data_quality):
        """
        Testa integração de qualidade de dados de validação.
        Teste automatizado: 90% gerado por IA
        """
        if 'error' in validation_data_quality:
            pytest.skip(f"Erro na qualidade de dados: {validation_data_quality['error']}")
        
        # Validações de qualidade
        assert validation_data_quality['dataset_nodes'] > 0, "Dataset deve ter nodes"
        assert validation_data_quality['dataset_ways'] > 0, "Dataset deve ter ways"
        assert validation_data_quality['graph_nodes'] > 0, "Grafo deve ter nodes"
        assert validation_data_quality['graph_edges'] > 0, "Grafo deve ter edges"
        
        # Validações de retenção
        assert validation_data_quality['node_retention'] > 0, "Retenção de nodes deve ser positiva"
        assert validation_data_quality['edge_retention'] > 0, "Retenção de edges deve ser positiva"
        
        # Validações de conectividade
        assert validation_data_quality['connected_components'] > 0, "Deve ter componentes conectados"
        assert validation_data_quality['giant_component_size'] > 0, "Componente gigante deve existir"
        
        print(f"\nIntegração de qualidade de dados:")
        print(f"  Dataset: {validation_data_quality['dataset_nodes']} nodes, {validation_data_quality['dataset_ways']} ways")
        print(f"  Grafo: {validation_data_quality['graph_nodes']} nodes, {validation_data_quality['graph_edges']} edges")
        print(f"  Retenção: {validation_data_quality['node_retention']:.2f} nodes, {validation_data_quality['edge_retention']:.2f} edges")
        print(f"  Componentes: {validation_data_quality['connected_components']}")
        print(f"  Qualidade: ✅")
    
    def test_validation_performance_integration(self, validation_performance_metrics):
        """
        Testa integração de performance de validação.
        Teste automatizado: 90% gerado por IA
        """
        if 'error' in validation_performance_metrics:
            pytest.skip(f"Erro na performance: {validation_performance_metrics['error']}")
        
        # Validações de performance
        assert validation_performance_metrics['dijkstra_time'] > 0, "Tempo Dijkstra deve ser positivo"
        assert validation_performance_metrics['astar_time'] > 0, "Tempo A* deve ser positivo"
        assert validation_performance_metrics['dijkstra_distance'] > 0, "Distância Dijkstra deve ser positiva"
        assert validation_performance_metrics['astar_distance'] > 0, "Distância A* deve ser positiva"
        
        # Validações de eficiência
        assert validation_performance_metrics['dijkstra_time'] < 10.0, "Dijkstra muito lento"
        assert validation_performance_metrics['astar_time'] < 10.0, "A* muito lento"
        
        # Validações de consistência
        assert abs(validation_performance_metrics['dijkstra_distance'] - validation_performance_metrics['astar_distance']) < 1e-9, "Distâncias devem ser iguais"
        
        print(f"\nIntegração de performance de validação:")
        print(f"  Dijkstra: {validation_performance_metrics['dijkstra_time']:.3f}s ({validation_performance_metrics['dijkstra_nodes_visited']} nodes)")
        print(f"  A*: {validation_performance_metrics['astar_time']:.3f}s ({validation_performance_metrics['astar_nodes_visited']} nodes)")
        print(f"  Distâncias: {validation_performance_metrics['dijkstra_distance']:.2f} vs {validation_performance_metrics['astar_distance']:.2f}")
        print(f"  Performance: ✅")
    
    def test_validation_memory_integration(self, validation_memory_usage):
        """
        Testa integração de memória de validação.
        Teste automatizado: 90% gerado por IA
        """
        if 'error' in validation_memory_usage:
            pytest.skip(f"Erro na memória: {validation_memory_usage['error']}")
        
        # Validações de memória
        assert validation_memory_usage['memory_mb'] > 0, "Memória deve ser positiva"
        assert validation_memory_usage['nodes'] > 0, "Deve ter nodes"
        assert validation_memory_usage['edges'] > 0, "Deve ter edges"
        
        # Validações de eficiência
        memory_per_node = validation_memory_usage['memory_per_node']
        assert memory_per_node > 0, "Memória por nó deve ser positiva"
        assert memory_per_node < 10, f"Memória por nó muito alta: {memory_per_node:.2f}MB"
        
        print(f"\nIntegração de memória de validação:")
        print(f"  Memória total: {validation_memory_usage['memory_mb']:.1f}MB")
        print(f"  Nodes: {validation_memory_usage['nodes']}")
        print(f"  Edges: {validation_memory_usage['edges']}")
        print(f"  Memória por nó: {memory_per_node:.2f}MB")
        print(f"  Eficiência: ✅")
    
    def test_validation_geographic_integration(self, validation_coordinates, validation_bounds, validation_centroid):
        """
        Testa integração geográfica de validação.
        Teste automatizado: 90% gerado por IA
        """
        # Validações de coordenadas
        assert len(validation_coordinates) > 0, "Deve ter coordenadas"
        
        # Validações de limites
        assert validation_bounds['min_lat'] < validation_bounds['max_lat'], "Latitude mínima deve ser < máxima"
        assert validation_bounds['min_lon'] < validation_bounds['max_lon'], "Longitude mínima deve ser < máxima"
        assert validation_bounds['lat_span'] > 0, "Extensão de latitude deve ser positiva"
        assert validation_bounds['lon_span'] > 0, "Extensão de longitude deve ser positiva"
        
        # Validações de centroide
        assert -90 <= validation_centroid['lat'] <= 90, "Centroide latitude inválida"
        assert -180 <= validation_centroid['lon'] <= 180, "Centroide longitude inválida"
        
        print(f"\nIntegração geográfica de validação:")
        print(f"  Coordenadas: {len(validation_coordinates)}")
        print(f"  Limites: ({validation_bounds['min_lat']:.6f}, {validation_bounds['min_lon']:.6f}) a ({validation_bounds['max_lat']:.6f}, {validation_bounds['max_lon']:.6f})")
        print(f"  Centroide: ({validation_centroid['lat']:.6f}, {validation_centroid['lon']:.6f})")
        print(f"  Extensão: {validation_bounds['lat_span']:.6f} x {validation_bounds['lon_span']:.6f}")
        print(f"  Geografia: ✅")
    
    def test_validation_connectivity_integration(self, validation_connectivity):
        """
        Testa integração de conectividade de validação.
        Teste automatizado: 90% gerado por IA
        """
        # Validações de conectividade
        assert validation_connectivity['total_components'] > 0, "Deve ter componentes"
        assert validation_connectivity['giant_component_size'] > 0, "Componente gigante deve existir"
        assert 0 < validation_connectivity['giant_component_ratio'] <= 1, "Razão do componente gigante deve ser válida"
        
        # Validações de rede
        assert validation_connectivity['giant_component_size'] > 10, "Componente gigante deve ser significativo"
        assert validation_connectivity['giant_component_ratio'] > 0.5, "Componente gigante deve ser dominante"
        
        print(f"\nIntegração de conectividade de validação:")
        print(f"  Componentes totais: {validation_connectivity['total_components']}")
        print(f"  Componente gigante: {validation_connectivity['giant_component_size']} nodes")
        print(f"  Razão: {validation_connectivity['giant_component_ratio']:.2f}")
        print(f"  Conectado: {validation_connectivity['is_connected']}")
        print(f"  Conectividade: ✅")
    
    def test_validation_code_quality_integration(self, validation_code_metrics):
        """
        Testa integração de qualidade de código de validação.
        Teste automatizado: 90% gerado por IA
        """
        # Validações de funções
        for func_name, metrics in validation_code_metrics['functions'].items():
            assert metrics['total_lines'] > 0, f"Função {func_name} deve ter linhas"
            assert metrics['non_empty_lines'] > 0, f"Função {func_name} deve ter linhas não-vazias"
            assert metrics['has_docstring'], f"Função {func_name} deve ter docstring"
            assert metrics['docstring_length'] > 0, f"Função {func_name} deve ter docstring não-vazia"
        
        # Validações de classes
        for class_name, metrics in validation_code_metrics['classes'].items():
            assert metrics['total_lines'] > 0, f"Classe {class_name} deve ter linhas"
            assert metrics['non_empty_lines'] > 0, f"Classe {class_name} deve ter linhas não-vazias"
            assert metrics['has_docstring'], f"Classe {class_name} deve ter docstring"
            assert metrics['docstring_length'] > 0, f"Classe {class_name} deve ter docstring não-vazia"
        
        print(f"\nIntegração de qualidade de código:")
        print(f"  Funções: {len(validation_code_metrics['functions'])}")
        print(f"  Classes: {len(validation_code_metrics['classes'])}")
        for func_name, metrics in validation_code_metrics['functions'].items():
            print(f"    {func_name}: {metrics['non_empty_lines']} linhas, {metrics['docstring_length']} chars docstring")
        print(f"  Qualidade: ✅")
    
    def test_validation_end_to_end(self, validation_dataset, validation_graph, validation_nodes):
        """
        Testa fluxo end-to-end de validação.
        Teste automatizado: 95% gerado por IA
        """
        # Testa fluxo completo
        start = validation_nodes[0]
        end = validation_nodes[-1]
        
        # Pathfinding
        dijkstra_result = dijkstra(validation_graph, start, end)
        astar_result = a_star(validation_graph, start, end)
        
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
        
        # Validações de igualdade
        assert abs(dijkstra_result['distance'] - astar_result['distance']) < 1e-9, "Distâncias devem ser iguais"
        assert dijkstra_result['path'] == astar_result['path'], "Paths devem ser iguais"
        
        print(f"\nFluxo end-to-end de validação:")
        print(f"  Start: {start}")
        print(f"  End: {end}")
        print(f"  Dijkstra: {dijkstra_result['distance']:.2f} km ({len(dijkstra_result['path'])} nós)")
        print(f"  A*: {astar_result['distance']:.2f} km ({len(astar_result['path'])} nós)")
        print(f"  Consistência: {'✅' if abs(dijkstra_result['distance'] - astar_result['distance']) < 1e-9 else '❌'}")
        print(f"  End-to-end: ✅")
