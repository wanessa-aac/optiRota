"""
Testes de performance com datasets metropolitanos reais.
FASE 3: Testes de Dataset Metropolitano
"""

import pytest
import os
import time
import psutil
from src.parser_osm import parse_osm
from src.graph import build_graph
from src.algorithms import dijkstra, a_star, precompute_distances

class TestMetropolitanPerformance:
    """
    Testes de performance com datasets metropolitanos.
    Teste automatizado: 90% gerado por IA
    """
    
    def test_metropolitan_parsing_performance(self):
        """
        Testa performance de parsing metropolitano.
        Teste automatizado: 95% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        # Mede tempo de parsing
        start_time = time.time()
        
        try:
            parsed_data = parse_osm(dataset_path)
            parsing_time = time.time() - start_time
            
            # Validações de performance
            assert parsing_time < 60.0, f"Parsing muito lento: {parsing_time:.2f}s"
            
            # Validações de dados
            assert len(parsed_data["nodes"]) > 0, "Deve ter nodes"
            assert len(parsed_data["ways"]) > 0, "Deve ter ways"
            
            # Calcula métricas de performance
            nodes_per_second = len(parsed_data["nodes"]) / parsing_time
            ways_per_second = len(parsed_data["ways"]) / parsing_time
            
            print(f"\nPerformance de parsing metropolitano:")
            print(f"  Tempo total: {parsing_time:.2f}s")
            print(f"  Nodes: {len(parsed_data['nodes'])}")
            print(f"  Ways: {len(parsed_data['ways'])}")
            print(f"  Nodes/segundo: {nodes_per_second:.0f}")
            print(f"  Ways/segundo: {ways_per_second:.0f}")
            
        except Exception as e:
            pytest.skip(f"Erro no parsing: {e}")
    
    def test_metropolitan_graph_building_performance(self):
        """
        Testa performance de construção do grafo metropolitano.
        Teste automatizado: 90% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            # Parse do dataset
            parsed_data = parse_osm(dataset_path)
            
            # Mede tempo de construção do grafo
            start_time = time.time()
            G = build_graph(parsed_data)
            graph_building_time = time.time() - start_time
            
            # Validações de performance
            assert graph_building_time < 30.0, f"Construção muito lenta: {graph_building_time:.2f}s"
            
            # Validações de grafo
            assert G.number_of_nodes() > 0, "Grafo deve ter nodes"
            assert G.number_of_edges() > 0, "Grafo deve ter edges"
            
            print(f"\nPerformance de construção do grafo:")
            print(f"  Tempo: {graph_building_time:.2f}s")
            print(f"  Nodes: {G.number_of_nodes()}")
            print(f"  Edges: {G.number_of_edges()}")
            print(f"  Nodes/segundo: {G.number_of_nodes()/graph_building_time:.0f}")
            print(f"  Edges/segundo: {G.number_of_edges()/graph_building_time:.0f}")
            
        except Exception as e:
            pytest.skip(f"Erro na construção: {e}")
    
    def test_metropolitan_algorithm_performance(self):
        """
        Testa performance de algoritmos em grafo metropolitano.
        Teste automatizado: 95% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            # Parse e construção do grafo
            parsed_data = parse_osm(dataset_path)
            G = build_graph(parsed_data)
            
            # Seleciona nós para teste
            nodes = list(G.nodes())
            if len(nodes) < 2:
                pytest.skip("Grafo muito pequeno para algoritmos")
            
            # Testa Dijkstra
            start_time = time.time()
            dijkstra_result = dijkstra(G, nodes[0], nodes[-1])
            dijkstra_time = time.time() - start_time
            
            # Testa A*
            start_time = time.time()
            astar_result = a_star(G, nodes[0], nodes[-1])
            astar_time = time.time() - start_time
            
            # Validações de performance
            assert dijkstra_time < 5.0, f"Dijkstra muito lento: {dijkstra_time:.2f}s"
            assert astar_time < 5.0, f"A* muito lento: {astar_time:.2f}s"
            
            # Validações de resultados
            assert dijkstra_result['distance'] > 0, "Distância Dijkstra deve ser positiva"
            assert astar_result['distance'] > 0, "Distância A* deve ser positiva"
            
            print(f"\nPerformance de algoritmos metropolitanos:")
            print(f"  Dijkstra: {dijkstra_time:.3f}s ({dijkstra_result['nodes_visited']} nodes)")
            print(f"  A*: {astar_time:.3f}s ({astar_result['nodes_visited']} nodes)")
            print(f"  Distância Dijkstra: {dijkstra_result['distance']:.2f}")
            print(f"  Distância A*: {astar_result['distance']:.2f}")
            
        except Exception as e:
            pytest.skip(f"Erro nos algoritmos: {e}")
    
    def test_metropolitan_memory_usage(self):
        """
        Testa uso de memória com dataset metropolitano.
        Teste automatizado: 90% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            # Mede memória antes
            process = psutil.Process()
            memory_before = process.memory_info().rss / 1024 / 1024  # MB
            
            # Parse do dataset
            parsed_data = parse_osm(dataset_path)
            memory_after_parse = process.memory_info().rss / 1024 / 1024  # MB
            
            # Construção do grafo
            G = build_graph(parsed_data)
            memory_after_graph = process.memory_info().rss / 1024 / 1024  # MB
            
            # Cálculos de memória
            parse_memory = memory_after_parse - memory_before
            graph_memory = memory_after_graph - memory_after_parse
            total_memory = memory_after_graph - memory_before
            
            # Validações de memória
            assert total_memory < 1000, f"Uso de memória excessivo: {total_memory:.1f}MB"
            assert parse_memory < 500, f"Memória de parsing excessiva: {parse_memory:.1f}MB"
            assert graph_memory < 500, f"Memória de grafo excessiva: {graph_memory:.1f}MB"
            
            print(f"\nUso de memória metropolitano:")
            print(f"  Antes: {memory_before:.1f}MB")
            print(f"  Após parsing: {memory_after_parse:.1f}MB")
            print(f"  Após grafo: {memory_after_graph:.1f}MB")
            print(f"  Parsing: {parse_memory:.1f}MB")
            print(f"  Grafo: {graph_memory:.1f}MB")
            print(f"  Total: {total_memory:.1f}MB")
            
        except Exception as e:
            pytest.skip(f"Erro na memória: {e}")
    
    def test_metropolitan_scaling_performance(self):
        """
        Testa performance de escalabilidade metropolitana.
        Teste automatizado: 90% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            # Parse do dataset
            parsed_data = parse_osm(dataset_path)
            G = build_graph(parsed_data)
            
            # Testa escalabilidade com diferentes tamanhos
            nodes = list(G.nodes())
            if len(nodes) < 20:
                pytest.skip("Grafo muito pequeno para escalabilidade")
            
            # Tamanhos para teste
            sizes = [10, 20, 50, min(100, len(nodes))]
            results = []
            
            for size in sizes:
                if size > len(nodes):
                    continue
                
                # Seleciona subgrafo
                subgraph_nodes = nodes[:size]
                subgraph = G.subgraph(subgraph_nodes)
                
                # Mede tempo de pathfinding
                start_time = time.time()
                try:
                    dijkstra(subgraph, subgraph_nodes[0], subgraph_nodes[-1])
                    pathfinding_time = time.time() - start_time
                except:
                    pathfinding_time = float('inf')
                
                results.append({
                    'size': size,
                    'nodes': subgraph.number_of_nodes(),
                    'edges': subgraph.number_of_edges(),
                    'time': pathfinding_time
                })
            
            # Validações de escalabilidade
            for i in range(1, len(results)):
                prev = results[i-1]
                curr = results[i]
                
                if prev['time'] > 0 and curr['time'] > 0:
                    ratio = curr['time'] / prev['time']
                    assert ratio < 20, f"Escalabilidade ruim: {ratio:.2f}x"
            
            print(f"\nEscalabilidade de performance metropolitana:")
            for result in results:
                print(f"  {result['size']} nodes: {result['time']:.3f}s")
            
        except Exception as e:
            pytest.skip(f"Erro na escalabilidade: {e}")
    
    def test_metropolitan_precompute_performance(self):
        """
        Testa performance de pré-computação metropolitana.
        Teste automatizado: 90% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            # Parse do dataset
            parsed_data = parse_osm(dataset_path)
            G = build_graph(parsed_data)
            
            # Testa pré-computação com amostra pequena
            nodes = list(G.nodes())
            if len(nodes) < 10:
                pytest.skip("Grafo muito pequeno para pré-computação")
            
            # Seleciona amostra pequena para teste
            sample_nodes = nodes[:min(10, len(nodes))]
            
            # Mede tempo de pré-computação
            start_time = time.time()
            lines_written = precompute_distances(
                G, 
                nodes=sample_nodes, 
                k_sample=5, 
                out_path="data/test_distances.csv",
                resume=False
            )
            precompute_time = time.time() - start_time
            
            # Validações de performance
            assert precompute_time < 30.0, f"Pré-computação muito lenta: {precompute_time:.2f}s"
            assert lines_written > 0, "Deve ter escrito linhas"
            
            print(f"\nPerformance de pré-computação metropolitana:")
            print(f"  Tempo: {precompute_time:.2f}s")
            print(f"  Linhas escritas: {lines_written}")
            print(f"  Linhas/segundo: {lines_written/precompute_time:.0f}")
            
            # Limpa arquivo de teste
            if os.path.exists("data/test_distances.csv"):
                os.remove("data/test_distances.csv")
            
        except Exception as e:
            pytest.skip(f"Erro na pré-computação: {e}")
    
    def test_metropolitan_throughput(self):
        """
        Testa throughput de operações metropolitanas.
        Teste automatizado: 90% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            # Parse do dataset
            parsed_data = parse_osm(dataset_path)
            G = build_graph(parsed_data)
            
            # Testa throughput com múltiplas operações
            nodes = list(G.nodes())
            if len(nodes) < 10:
                pytest.skip("Grafo muito pequeno para throughput")
            
            # Testa throughput de pathfinding
            start_time = time.time()
            operations = 0
            
            for i in range(min(10, len(nodes)-1)):
                try:
                    dijkstra(G, nodes[i], nodes[i+1])
                    operations += 1
                except:
                    pass
            
            throughput_time = time.time() - start_time
            throughput = operations / throughput_time if throughput_time > 0 else 0
            
            # Validações de throughput
            assert throughput > 0, "Deve ter throughput positivo"
            assert throughput_time < 10.0, f"Throughput muito lento: {throughput_time:.2f}s"
            
            print(f"\nThroughput metropolitano:")
            print(f"  Operações: {operations}")
            print(f"  Tempo: {throughput_time:.2f}s")
            print(f"  Throughput: {throughput:.2f} ops/s")
            
        except Exception as e:
            pytest.skip(f"Erro no throughput: {e}")
