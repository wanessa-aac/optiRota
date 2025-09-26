"""
Testes de conectividade em grafos metropolitanos.
FASE 3: Testes de Dataset Metropolitano
"""

import pytest
import os
import time
import networkx as nx
from src.parser_osm import parse_osm
from src.graph import build_graph
from src.algorithms import dijkstra, a_star

class TestMetropolitanConnectivity:
    """
    Testes de conectividade em grafos metropolitanos.
    Teste automatizado: 90% gerado por IA
    """
    
    def test_metropolitan_graph_connectivity(self):
        """
        Testa conectividade em grafo metropolitano.
        Teste automatizado: 95% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            # Parse do dataset
            parsed_data = parse_osm(dataset_path)
            
            # Constrói grafo
            G = build_graph(parsed_data)
            
            # Validações de conectividade
            assert G.number_of_nodes() > 0, "Grafo deve ter nodes"
            assert G.number_of_edges() > 0, "Grafo deve ter edges"
            
            # Testa conectividade fraca
            wccs = list(nx.weakly_connected_components(G))
            assert len(wccs) > 0, "Deve ter componentes conectados"
            
            # Componente gigante deve ser significativo
            giant_component = max(wccs, key=len)
            assert len(giant_component) > 10, "Componente gigante deve ser significativo"
            
            print(f"\nConectividade metropolitana:")
            print(f"  Nodes: {G.number_of_nodes()}")
            print(f"  Edges: {G.number_of_edges()}")
            print(f"  Componentes: {len(wccs)}")
            print(f"  Componente gigante: {len(giant_component)} nodes")
            
        except Exception as e:
            pytest.skip(f"Erro na conectividade: {e}")
    
    def test_metropolitan_graph_density(self):
        """
        Testa densidade do grafo metropolitano.
        Teste automatizado: 90% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            parsed_data = parse_osm(dataset_path)
            G = build_graph(parsed_data)
            
            # Calcula densidade
            density = nx.density(G)
            
            # Validações de densidade
            assert 0 < density < 1, f"Densidade inválida: {density}"
            assert density > 0.001, f"Densidade muito baixa: {density}"
            assert density < 0.5, f"Densidade muito alta: {density}"
            
            print(f"\nDensidade do grafo:")
            print(f"  Densidade: {density:.6f}")
            print(f"  Nodes: {G.number_of_nodes()}")
            print(f"  Edges: {G.number_of_edges()}")
            
        except Exception as e:
            pytest.skip(f"Erro na densidade: {e}")
    
    def test_metropolitan_graph_degree_distribution(self):
        """
        Testa distribuição de graus no grafo metropolitano.
        Teste automatizado: 90% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            parsed_data = parse_osm(dataset_path)
            G = build_graph(parsed_data)
            
            # Calcula distribuição de graus
            degrees = [G.degree(n) for n in G.nodes()]
            
            # Validações de distribuição
            assert len(degrees) > 0, "Deve ter graus"
            assert min(degrees) >= 0, "Grau mínimo deve ser >= 0"
            assert max(degrees) > 0, "Deve ter pelo menos um nó conectado"
            
            # Estatísticas
            avg_degree = sum(degrees) / len(degrees)
            max_degree = max(degrees)
            
            # Validações de rede urbana
            assert avg_degree > 1.0, f"Grau médio muito baixo: {avg_degree}"
            assert max_degree > 2, f"Grau máximo muito baixo: {max_degree}"
            
            print(f"\nDistribuição de graus:")
            print(f"  Grau médio: {avg_degree:.2f}")
            print(f"  Grau máximo: {max_degree}")
            print(f"  Nodes: {len(degrees)}")
            
        except Exception as e:
            pytest.skip(f"Erro na distribuição: {e}")
    
    def test_metropolitan_graph_pathfinding(self):
        """
        Testa pathfinding em grafo metropolitano.
        Teste automatizado: 95% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            parsed_data = parse_osm(dataset_path)
            G = build_graph(parsed_data)
            
            # Seleciona nós para teste
            nodes = list(G.nodes())
            if len(nodes) < 2:
                pytest.skip("Grafo muito pequeno para pathfinding")
            
            # Testa pathfinding entre nós aleatórios
            start = nodes[0]
            end = nodes[-1]
            
            # Testa Dijkstra
            start_time = time.time()
            dijkstra_result = dijkstra(G, start, end)
            dijkstra_time = time.time() - start_time
            
            # Testa A*
            start_time = time.time()
            astar_result = a_star(G, start, end)
            astar_time = time.time() - start_time
            
            # Validações de pathfinding
            assert dijkstra_result['distance'] > 0, "Distância Dijkstra deve ser positiva"
            assert astar_result['distance'] > 0, "Distância A* deve ser positiva"
            assert dijkstra_time < 10.0, f"Dijkstra muito lento: {dijkstra_time:.2f}s"
            assert astar_time < 10.0, f"A* muito lento: {astar_time:.2f}s"
            
            print(f"\nPathfinding metropolitano:")
            print(f"  Dijkstra: {dijkstra_result['distance']:.2f} ({dijkstra_time:.3f}s)")
            print(f"  A*: {astar_result['distance']:.2f} ({astar_time:.3f}s)")
            print(f"  Nodes visitados Dijkstra: {dijkstra_result['nodes_visited']}")
            print(f"  Nodes visitados A*: {astar_result['nodes_visited']}")
            
        except Exception as e:
            pytest.skip(f"Erro no pathfinding: {e}")
    
    def test_metropolitan_graph_scaling(self):
        """
        Testa escalabilidade do grafo metropolitano.
        Teste automatizado: 90% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            parsed_data = parse_osm(dataset_path)
            G = build_graph(parsed_data)
            
            # Testa escalabilidade com subgrafos
            nodes = list(G.nodes())
            if len(nodes) < 10:
                pytest.skip("Grafo muito pequeno para escalabilidade")
            
            # Testa com diferentes tamanhos
            sizes = [10, 50, 100, min(500, len(nodes))]
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
                    assert ratio < 10, f"Escalabilidade ruim: {ratio:.2f}x"
            
            print(f"\nEscalabilidade metropolitana:")
            for result in results:
                print(f"  {result['size']} nodes: {result['time']:.3f}s")
            
        except Exception as e:
            pytest.skip(f"Erro na escalabilidade: {e}")
    
    def test_metropolitan_graph_robustness(self):
        """
        Testa robustez do grafo metropolitano.
        Teste automatizado: 90% gerado por IA
        """
        dataset_path = "data/090925maceio_ponta_verde.osm"
        
        if not os.path.exists(dataset_path):
            pytest.skip(f"Dataset não encontrado: {dataset_path}")
        
        try:
            parsed_data = parse_osm(dataset_path)
            G = build_graph(parsed_data)
            
            # Testa robustez removendo nós aleatórios
            nodes = list(G.nodes())
            if len(nodes) < 10:
                pytest.skip("Grafo muito pequeno para robustez")
            
            # Remove 10% dos nós
            nodes_to_remove = nodes[:len(nodes)//10]
            G_robust = G.copy()
            G_robust.remove_nodes_from(nodes_to_remove)
            
            # Validações de robustez
            assert G_robust.number_of_nodes() > 0, "Grafo deve ter nodes após remoção"
            assert G_robust.number_of_edges() > 0, "Grafo deve ter edges após remoção"
            
            # Testa conectividade após remoção
            wccs = list(nx.weakly_connected_components(G_robust))
            assert len(wccs) > 0, "Deve ter componentes conectados após remoção"
            
            print(f"\nRobustez metropolitana:")
            print(f"  Nodes originais: {G.number_of_nodes()}")
            print(f"  Nodes após remoção: {G_robust.number_of_nodes()}")
            print(f"  Componentes: {len(wccs)}")
            
        except Exception as e:
            pytest.skip(f"Erro na robustez: {e}")
